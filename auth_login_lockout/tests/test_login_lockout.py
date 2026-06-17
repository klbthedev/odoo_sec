from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestLoginLockout(TransactionCase):

    def setUp(self):
        super().setUp()

        self.user = self.env["res.users"].create({
            "name": "Lockout User",
            "login": "lockout@example.com",
            "password": "secret123",
        })

    def test_lock_computation(self):
        self.user.login_locked_until = (
            fields.Datetime.now()
            + timedelta(minutes=5)
        )

        self.assertTrue(
            self.user.is_login_locked
        )

    def test_unlock_after_expiry(self):
        self.user.login_locked_until = (
            fields.Datetime.now()
            - timedelta(minutes=1)
        )

        self.assertFalse(
            self.user.is_login_locked
        )

    def test_reset_lockout(self):
        self.user.write({
            "failed_login_attempts": 4,
        })

        self.user._reset_login_lockout()
        self.assertEqual(self.user.failed_login_attempts,0,)
        self.assertFalse(self.user.login_locked_until)