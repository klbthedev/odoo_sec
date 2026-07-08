from odoo import models


class IrUiMenu(models.Model):
    _inherit = ["ir.ui.menu", "security.guarded.mixin"]
