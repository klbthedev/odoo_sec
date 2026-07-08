from odoo import models


class IrModelAccess(models.Model):
    _inherit = ["ir.model.access", "security.guarded.mixin"]
