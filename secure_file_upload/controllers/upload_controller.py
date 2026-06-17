import base64
from odoo import http
from odoo.http import request

class SecureUploadController(http.Controller):

    @http.route("/secure/upload", type="json", auth="user", methods=["POST"])
    def upload_file(self, file, filename):
        data = {
            "name": filename,
            "datas": file,  # base64 expected
            "res_model": "ir.attachment",
        }

        attachment = request.env["ir.attachment"].sudo().create(data)

        return {
            "id": attachment.id,
            "name": attachment.name,
        }