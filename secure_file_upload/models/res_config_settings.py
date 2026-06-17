from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    max_upload_size = fields.Integer(
        string="Max File Size (Bytes)",
        config_parameter="secure_upload.max_size",
        default=10 * 1024 * 1024,
    )

    allowed_extensions = fields.Char(
        string="Allowed Extensions",
        config_parameter="secure_upload.allowed_ext",
        default="jpg,jpeg,png,pdf,webp,pem,key",
    )

    enable_rate_limit = fields.Boolean(
        string="Enable Upload Rate Limiting",
        config_parameter="secure_upload.rate_limit",
    )

    max_uploads_per_minute = fields.Integer(
        config_parameter="secure_upload.max_per_minute",
        default=20,
    )

    max_upload_size_per_hour = fields.Integer(
        config_parameter="secure_upload.max_hour_size",
        default=100 * 1024 * 1024,
    )

    reject_suspicious = fields.Boolean(
        config_parameter="secure_upload.reject_suspicious",
        default=True,
    )