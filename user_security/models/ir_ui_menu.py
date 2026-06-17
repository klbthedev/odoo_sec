from odoo import models
from odoo.exceptions import AccessError


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    def _check_security_admin(self):
        if self.env.su:
            return
        if self.env.user.has_group("user_security.group_security_admin"):
            return
        raise AccessError("Menu modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()