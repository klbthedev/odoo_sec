from odoo import models, fields

class SecureUploadAudit(models.Model):
    _name = "secure.upload.audit"
    _description = "Secure Upload Audit Log"
    _order = "create_date desc"

    user_id = fields.Many2one("res.users")
    filename = fields.Char()
    file_size = fields.Integer()
    mime_type = fields.Char()
    result = fields.Selection([
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("flagged", "Flagged"),
    ])
    reason = fields.Text()
    timestamp = fields.Datetime(default=fields.Datetime.now)
    ip_address = fields.Char()