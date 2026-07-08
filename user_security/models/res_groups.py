from odoo import models


class ResGroups(models.Model):
    _inherit = ["res.groups", "security.guarded.mixin"]
