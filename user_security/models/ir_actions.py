from odoo import models
from odoo.exceptions import AccessError


class SecurityActionMixin:
    def _check_security_admin(self):
        if self.env.su:
            return
        if self.env.user.has_group("user_security.group_security_admin"):
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


class IrActionsActWindow(models.Model,SecurityActionMixin):
    _inherit = "ir.actions.act_window"


class IrActionsServer(models.Model,SecurityActionMixin):
    _inherit = "ir.actions.server"


class IrActionsClient(models.Model,SecurityActionMixin):
    _inherit = "ir.actions.client"


class IrActionsReport(models.Model,SecurityActionMixin):
    _inherit = "ir.actions.report"


class IrActionsUrl(models.Model,SecurityActionMixin):
    _inherit = "ir.actions.act_url"