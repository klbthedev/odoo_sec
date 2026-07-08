from odoo import models


class IrRule(models.Model):
    _name = "ir.rule"
    _inherit = ["ir.rule", "security.guarded.mixin"]
