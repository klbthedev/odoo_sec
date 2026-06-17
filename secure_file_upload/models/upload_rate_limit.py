from odoo import models, fields, api
from collections import defaultdict
import time

class UploadRateLimit(models.Model):
    _name = "secure.upload.rate"
    _description = "Upload Rate Tracking"

    user_id = fields.Many2one("res.users")
    timestamp = fields.Float()
    size = fields.Integer()