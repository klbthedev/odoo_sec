import logging
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    failed_login_attempts = fields.Integer(
        string="Failed Login Attempts",
        default=0,
        copy=False,
        readonly=True,
    )

    login_locked_until = fields.Datetime(
        string="Locked Until",
        copy=False,
        readonly=True,
    )

    is_login_locked = fields.Boolean(
        string="Login Locked",
        compute="_compute_is_login_locked",
    )

    lockout_count = fields.Integer(
        string="Lockout Count",
        default=0,
        copy=False,
        readonly=True,
    )

    is_permanently_blocked = fields.Boolean(
        string="Permanently Blocked",
        default=False,
        copy=False,
        readonly=True,
    )

    security_status = fields.Selection(
        [
            ("ok", "OK"),
            ("locked", "Temporarily Locked"),
            ("blocked", "Permanently Blocked"),
        ],
        compute="_compute_security_status",
        store=True,
    )

    @api.model
    def _get_max_lockouts(self):
        return int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("auth_login_lockout.login_lockout_max_lockouts",3,)
        )
    
    def _block_user(self):
        self.ensure_one()
        self.sudo().write({
            "is_permanently_blocked": True,
            "login_locked_until": False,
        })
        _logger.warning("User %s permanently blocked",self.login,)

    def action_unblock_user(self):
        self.ensure_one()
        self.sudo().write({
            "failed_login_attempts": 0,
            "login_locked_until": False,
            "lockout_count": 0,
            "is_permanently_blocked": False,
        })
        _logger.info("User %s manually unblocked",self.login,)

    @api.depends("login_locked_until","is_permanently_blocked",)
    def _compute_security_status(self):
        now = fields.Datetime.now()
        for user in self:
            if user.is_permanently_blocked:
                user.security_status = "blocked"
            elif (user.login_locked_until and now < user.login_locked_until):
                user.security_status = "locked"
            else:
                user.security_status = "ok"


    @api.depends("login_locked_until")
    def _compute_is_login_locked(self):
        now = fields.Datetime.now()

        for user in self:
            user.is_login_locked = bool(
                user.login_locked_until
                and now < user.login_locked_until
            )

    @api.model
    def _get_lockout_max_attempts(self):
        return int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "auth_login_lockout.login_lockout_max_attempts",
                5,
            )
        )

    @api.model
    def _get_lockout_duration(self):
        return int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "auth_login_lockout.login_lockout_duration",
                15,
            )
        )

    @api.model
    def _exclude_admins(self):
        value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "auth_login_lockout.login_lockout_exclude_admins",
                "True",
            )
        )

        return str(value).lower() in (
            "1",
            "true",
            "yes",
        )

    def _is_lockout_exempt(self):
        self.ensure_one()

        if not self._exclude_admins():
            return False

        return self.has_group("base.group_system")

    def _is_account_locked(self):
        self.ensure_one()

        if not self.login_locked_until:
            return False

        return fields.Datetime.now() < self.login_locked_until

    def _reset_lockout(self):
        self.ensure_one()

        self.sudo().write({
            "failed_login_attempts": 0,
            "login_locked_until": False,
        })

        _logger.info("Lockout reset for user %s",self.login,)

    def _increment_failed_attempts(self):
        self.ensure_one()
        if self._is_lockout_exempt():
            return
        self.env.cr.execute(
            """
            SELECT id
              FROM res_users
             WHERE id = %s
             FOR UPDATE
            """,
            [self.id],
        )
        self.invalidate_cache()
        attempts = self.failed_login_attempts + 1
        values = {
            "failed_login_attempts": attempts,
        }
        max_attempts = self._get_lockout_max_attempts()
        # if attempts >= max_attempts:
        #     duration = self._get_lockout_duration()
        #     locked_until = (fields.Datetime.now() + timedelta(minutes=duration))
        #     values["login_locked_until"] = locked_until
        #     _logger.warning("User %s locked until %s",self.login,locked_until,)
        if attempts >= max_attempts:
            lockout_count = self.lockout_count + 1
            max_lockouts = self._get_max_lockouts()
            values.update({
                "lockout_count": lockout_count,
                "failed_login_attempts": 0,
            })
            if lockout_count >= max_lockouts:
                values.update({
                    "is_permanently_blocked": True,
                    "login_locked_until": False,
                })
                _logger.warning("User %s permanently blocked (%s/%s lockouts)",self.login,lockout_count,max_lockouts,)
            else:
                duration = self._get_lockout_duration()
                locked_until = (fields.Datetime.now() + timedelta(minutes=duration))
                values["login_locked_until"] = locked_until
                _logger.warning("User %s locked until %s (lockout %s/%s)",self.login,locked_until,lockout_count,max_lockouts,)
                
        self.sudo().write(values)
        _logger.info("Failed login %s (%s/%s)",self.login,attempts,max_attempts,)

    # def _check_lockout_before_login(self):
    #     self.ensure_one()
    #     if self._is_account_locked():
    #         _logger.warning(
    #             "Blocked login for locked user %s",
    #             self.login,
    #         )
    #         raise AccessDenied(_("Your account has been temporarily locked due to multiple failed login attempts. Please try again later."))
    def _check_lockout_before_login(self):
        self.ensure_one()
        if self.is_permanently_blocked:
            raise AccessDenied(_("Your account has been blocked. Please contact your administrator."))
        if self._is_account_locked():
            raise AccessDenied(_("Your account has been temporarily locked due to multiple failed login attempts. Please try again later."))

    def _check_credentials(self, password, env):
        #Compatible with Odoo versions that use _check_credentials(password, env)This hook is executed during password validation.
        self.ensure_one()
        self._check_lockout_before_login()

        try:
            result = super()._check_credentials(password,env,)

            if (self.failed_login_attempts or self.login_locked_until):
                self._reset_lockout()

            return result

        except AccessDenied:
            self._increment_failed_attempts()
            raise

    def _check_credentials_for_uid(self,password,user_agent_env=None,):

        self.ensure_one()

        self._check_lockout_before_login()

        try:
            result = super()._check_credentials_for_uid(password,user_agent_env=user_agent_env,)

            if (self.failed_login_attempts or self.login_locked_until):
                self._reset_lockout()

            return result

        except AccessDenied:
            self._increment_failed_attempts()
            raise