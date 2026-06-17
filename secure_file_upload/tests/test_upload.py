from odoo.tests.common import TransactionCase
import base64

class TestUploadSecurity(TransactionCase):

    def test_valid_upload(self):
        data = base64.b64encode(b"valid file content")
        att = self.env["ir.attachment"].create({
            "name": "test.pdf",
            "datas": data,
        })
        self.assertTrue(att)

    def test_oversized_file(self):
        with self.assertRaises(Exception):
            self.env["ir.attachment"].create({
                "name": "big.pdf",
                "datas": base64.b64encode(b"x" * 20_000_000),
            })

    def test_double_extension_block(self):
        with self.assertRaises(Exception):
            self.env["ir.attachment"].create({
                "name": "file.pdf.exe",
                "datas": base64.b64encode(b"x"),
            })

    def test_image_validation(self):
        # corrupted image
        with self.assertRaises(Exception):
            self.env["ir.attachment"].create({
                "name": "img.png",
                "datas": base64.b64encode(b"not-an-image"),
            })