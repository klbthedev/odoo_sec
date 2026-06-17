from odoo import models
from odoo.exceptions import AccessError


class SecurityActionMixin(models.AbstractModel):
    _name = "security.action.mixin"
    _description = "Security Action Mixin"


    def _check_security_admin(self):
        if (self.env.su or self.env.user.has_group("user_security.group_security_admin") or self.env.user.has_group("base.group_system")):
            return
        raise AccessError("Action modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()


class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.act_window"

    def _check_security_admin(self):
        if (self.env.su or self.env.user.has_group("user_security.group_security_admin") or self.env.user.has_group("base.group_system")):
            return
        raise AccessError("Action modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()


class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.server"

    def _check_security_admin(self):
        if (self.env.su or self.env.user.has_group("user_security.group_security_admin") or self.env.user.has_group("base.group_system")):
            return
        raise AccessError("Action modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()


class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.client"

    def _check_security_admin(self):
        if (self.env.su or self.env.user.has_group("user_security.group_security_admin") or self.env.user.has_group("base.group_system")):
            return
        raise AccessError("Action modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()

class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.report"

    def _check_security_admin(self):
        if (self.env.su or self.env.user.has_group("user_security.group_security_admin") or self.env.user.has_group("base.group_system")):
            return
        raise AccessError("Action modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()

class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.act_url"

    def _check_security_admin(self):
        if (self.env.su or self.env.user.has_group("user_security.group_security_admin") or self.env.user.has_group("base.group_system")):
            return
        raise AccessError("Action modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()


