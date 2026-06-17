from odoo import models
from odoo.exceptions import AccessError


class IrRule(models.Model):
    _inherit = "ir.rule"

    def _check_security_admin(self):
        if self.env.su:
            return
        if self.env.user.has_group("user_security.group_security_admin"):
            return
        raise AccessError("Record rule modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()

    
    def _check(self):
        if (not self.env.su and not self.env.user.has_group('user_security.group_security_admin')):
            raise AccessError("Rule modification denied.")

    def create(self, vals):
        self._check()
        return super().create(vals)

    def write(self, vals):
        self._check()
        return super().write(vals)

    def unlink(self):
        self._check()
        return super().unlink()