from odoo import models, fields, api
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = "res.users"

    # PROTECTED_FIELDS = {
    #     "groups_id",
    #     "active",
    #     "company_id",
    #     "company_ids",
    #     "share",
    # }

    # PROTECTED_USERS = {
    #     1,
    #     2,
    # }

    # def _check_security_admin(self):
    #     if self.env.su:
    #         return
    #     if self.env.user.has_group("user_security.group_security_admin"):
    #         return
    #     raise AccessError("Only Security Administrators may modify security settings.")

    # def write(self, vals):
    #     if self.PROTECTED_FIELDS.intersection(vals):
    #         self._check_security_admin()
    #     if any(user.id in self.PROTECTED_USERS for user in self):
    #         self._check_security_admin()
    #     return super().write(vals)

    # def unlink(self):
    #     if any(user.id in self.PROTECTED_USERS for user in self):
    #         self._check_security_admin()
    #     return super().unlink()


    security_protected = fields.Boolean(default=False,copy=False)

    SENSITIVE_FIELDS = {
        'groups_id',
        'active',
        'company_id',
        'company_ids',
        'share',
        'login',
        'password',
        'active',
        'company_id',
        'company_ids',
        'share',
        'login',
        'password',
        'partner_id',
    }

    def _is_security_admin(self):
        return (self.env.su 
            or self.env.user.has_group('user_security.group_security_admin')
            or self.env.user.has_group('base.group_system')
        )

    def _check_protected(self):
        if self._is_security_admin():
            return
        protected_users = self.filtered(
            lambda u:
                u.security_protected
                or
                u.id in (1, 2)
        )
        if protected_users:
            raise AccessError("Protected user account.")

    def write(self, vals):
        self._check_protected()
        if (self.SENSITIVE_FIELDS.intersection(vals) and not self._is_security_admin()):
            raise AccessError("Security modification denied.")
        return super().write(vals)

    def unlink(self):
        self._check_protected()
        return super().unlink()
    
    
    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            if user.id in (1, 2):
                user.sudo().security_protected = True
        return users