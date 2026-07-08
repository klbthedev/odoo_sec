from odoo import _, api, models
from odoo.exceptions import AccessError


class SecurityGuardedMixin(models.AbstractModel):
    """Restrict create/write/unlink to Security Administrators.

    Any model that mixes this in can only be modified by a Security
    Administrator (``user_security.group_security_admin``) or from a
    superuser / sudo context (module install & upgrade, automated jobs,
    ``set_param`` and other elevated flows). This keeps legitimate system
    automation working while preventing regular administrators from tampering
    with security-governing configuration.
    """

    _name = "security.guarded.mixin"
    _description = "Security Guarded Mixin"

    def _is_security_admin(self):
        return self.env.su or self.env.user.has_group(
            "user_security.group_security_admin"
        )

    def _check_security_admin(self):
        if not self._is_security_admin():
            raise AccessError(
                _(
                    "Only Security Administrators may modify security "
                    "configuration (%s).",
                    self._description or self._name,
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        self._check_security_admin()
        return super().create(vals_list)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()
