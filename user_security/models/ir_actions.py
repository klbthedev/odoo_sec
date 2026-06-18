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


class IrActionsServer(models.Model):
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


class IrActionsClient(models.Model):
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

class IrActionsReport(models.Model):
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

class IrActionsActUrl(models.Model):
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


class SecurityProtectedMixin(models.AbstractModel):
    _name = "security.protected.mixin"
    _description = "Security Protected Mixin"

    def _check_security_admin(self):
        if self.env.su:
            return

        if self.env.user.has_group("user_security.group_security_admin"):
            return

        raise AccessError("Only Security Administrators may modify security configuration.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()

class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _check_security_admin(self):
        if self.env.su or self.env.user.has_group("user_security.group_security_admin"):
            return
        raise AccessError("View modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()

class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    def _check_security_admin(self):
        if self.env.su or self.env.user.has_group("user_security.group_security_admin"):
            return
        raise AccessError("Field modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()


class IrCron(models.Model):
    _inherit = "ir.cron"

    def _check_security_admin(self):
        if self.env.su or self.env.user.has_group("user_security.group_security_admin"):
            return
        raise AccessError("Cron modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()

class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def _check_security_admin(self):
        if self.env.su or self.env.user.has_group("user_security.group_security_admin"):
            return
        raise AccessError("System parameter modification denied.")

    def create(self, vals):
        self._check_security_admin()
        return super().create(vals)

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

    def unlink(self):
        self._check_security_admin()
        return super().unlink()

class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def _check_security_admin(self):
        if self.env.su or self.env.user.has_group("user_security.group_security_admin") or self.env.user.has_group("base.group_system"):
            return
        raise AccessError("Module installation denied.")

    def write(self, vals):
        self._check_security_admin()
        return super().write(vals)

# class BaseAutomation(models.Model):
#     _inherit = "base.automation"

#     def _check_security_admin(self):
#         if self.env.su or self.env.user.has_group(
#             "user_security.group_security_admin"
#         ):
#             return
#         raise AccessError("Automation modification denied.")

#     def create(self, vals):
#         self._check_security_admin()
#         return super().create(vals)

#     def write(self, vals):
#         self._check_security_admin()
#         return super().write(vals)

#     def unlink(self):
#         self._check_security_admin()
#         return super().unlink()
