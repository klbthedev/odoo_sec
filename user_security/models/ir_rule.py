from odoo import models


class IrRule(models.Model):
    _inherit = ["ir.rule", "security.guarded.mixin"]
