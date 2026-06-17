import base64
import time
import logging
import mimetypes

from odoo import models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

SUSPICIOUS_PATTERNS = [
    b"eval(",
    b"<script",
    b"powershell",
    b"cmd.exe",
    b"bash",
    b"BEGIN PRIVATE KEY",
]

class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._validate_upload(vals, stage="create")
        return super().create(vals_list)

    def write(self, vals):
        if "datas" in vals:
            for rec in self:
                rec._validate_upload(vals, stage="write")
        return super().write(vals)

    def _validate_upload(self, vals, stage="create"):
        config = self.env["ir.config_parameter"].sudo()

        max_size = int(config.get_param("secure_upload.max_size", 10_485_760))
        allowed_ext = config.get_param("secure_upload.allowed_ext", "")
        allowed_ext = [x.strip().lower() for x in allowed_ext.split(",") if x]

        reject_suspicious = config.get_param("secure_upload.reject_suspicious") == "True"
        rate_limit_enabled = config.get_param("secure_upload.rate_limit") == "True"

        name = vals.get("name", "unknown")
        data = vals.get("datas")

        if not data:
            return

        file_bytes = base64.b64decode(data)

        if len(file_bytes) > max_size:
            self._audit(name, len(file_bytes), None, "rejected", "File too large")
            raise ValidationError("File exceeds maximum allowed size.")

        ext = (name.split(".")[-1] if "." in name else "").lower()
        mime, _ = mimetypes.guess_type(name)
        mime = mime or "application/octet-stream"

        if rate_limit_enabled:
            self._check_rate_limit(len(file_bytes))

        if allowed_ext and ext not in allowed_ext:
            self._audit(name, len(file_bytes), mime, "rejected", "Extension not allowed")
            raise ValidationError("File type not allowed.")

        if name.count(".") > 1:
            if not self._mime_matches_ext(ext, mime):
                self._audit(name, len(file_bytes), mime, "rejected", "Double extension mismatch")
                raise ValidationError("Suspicious file name detected.")

        if reject_suspicious:
            for p in SUSPICIOUS_PATTERNS:
                if p in file_bytes:
                    self._audit(name, len(file_bytes), mime, "rejected", "Suspicious content")
                    raise ValidationError("Malicious content detected.")

        if ext == "pdf":
            self._validate_pdf(file_bytes)

        if ext in ["jpg", "jpeg", "png", "webp"]:
            vals["datas"] = self._validate_image(file_bytes)

        self._audit(name, len(file_bytes), mime, "accepted", "OK")

    def _check_rate_limit(self, size):
        user = self.env.user
        now = time.time()

        per_min = int(self.env["ir.config_parameter"].sudo().get_param(
            "secure_upload.max_per_minute", 20
        ))
        per_hour_size = int(self.env["ir.config_parameter"].sudo().get_param(
            "secure_upload.max_hour_size", 100 * 1024 * 1024
        ))

        recs = self.env["secure.upload.rate"].sudo().search([
            ("user_id", "=", user.id),
            ("timestamp", ">", now - 3600),
        ])

        if len([r for r in recs if r.timestamp > now - 60]) > per_min:
            raise ValidationError("Upload rate limit exceeded (per minute).")

        total_size = sum(recs.mapped("size")) + size
        if total_size > per_hour_size:
            raise ValidationError("Hourly upload size limit exceeded.")

        self.env["secure.upload.rate"].sudo().create({
            "user_id": user.id,
            "timestamp": now,
            "size": size,
        })

    def _mime_matches_ext(self, ext, mime):
        mapping = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "pdf": "application/pdf",
            "webp": "image/webp",
        }
        return mapping.get(ext) == mime

    def _validate_pdf(self, data):
        lowered = data.lower()
        dangerous = [
            b"/javascript",
            b"/launch",
            b"/openaction",
            b"/embeddedfile",
        ]

        for d in dangerous:
            if d in lowered:
                self._audit("pdf", len(data), "application/pdf", "rejected", "Unsafe PDF")
                raise ValidationError("Unsafe PDF content detected.")

    def _validate_image(self, data):
        from PIL import Image
        import io

        try:
            img = Image.open(io.BytesIO(data))
            img.verify()
        except Exception:
            raise ValidationError("Corrupted image file.")

        img = Image.open(io.BytesIO(data))
        out = io.BytesIO()
        img.save(out, format=img.format)
        return base64.b64encode(out.getvalue()).decode()

    def _audit(self, filename, size, mime, result, reason):
        self.env["secure.upload.audit"].sudo().create({
            "user_id": self.env.user.id,
            "filename": filename,
            "file_size": size,
            "mime_type": mime,
            "result": result,
            "reason": reason,
        })