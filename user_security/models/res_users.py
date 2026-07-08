from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = "res.users"

    security_protected = fields.Boolean(
        string="Security Protected",
        default=False,
        copy=False,
        help="Protected accounts can only be modified or deleted by a "
             "Security Administrator.",
    )

    # Fields that govern authentication, access rights and multi-company
    # isolation. They must never be changed by a non Security Administrator.
    SENSITIVE_FIELDS = {
        "groups_id",
        "active",
        "company_id",
        "company_ids",
        "share",
        "login",
        "partner_id",
    }

    def _is_security_admin(self):
        return self.env.su or self.env.user.has_group(
            "user_security.group_security_admin"
        )

    def _protected_user_ids(self):
        """Ids of always-protected system accounts (superuser & admin)."""
        ids = []
        for xml_id in ("base.user_root", "base.user_admin"):
            user = self.env.ref(xml_id, raise_if_not_found=False)
            if user:
                ids.append(user.id)
        return ids

    def _check_protected(self):
        if self._is_security_admin():
            return
        protected = self.filtered(
            lambda u: u.security_protected or u.id in self._protected_user_ids()
        )
        if protected:
            raise AccessError(
                _(
                    "This user account is protected and can only be modified "
                    "by a Security Administrator."
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        if not self._is_security_admin():
            raise AccessError(
                _("Only Security Administrators may create users.")
            )
        return super().create(vals_list)

    def write(self, vals):
        self._check_protected()
        if not self._is_security_admin():
            sensitive = self.SENSITIVE_FIELDS.intersection(vals)
            if sensitive:
                raise AccessError(
                    _(
                        "Only Security Administrators may modify "
                        "security-sensitive user fields (%s).",
                        ", ".join(sorted(sensitive)),
                    )
                )
            # A user may reset their own password, but not anyone else's.
            if "password" in vals and any(u.id != self.env.uid for u in self):
                raise AccessError(
                    _(
                        "Only Security Administrators may reset another "
                        "user's password."
                    )
                )
        return super().write(vals)

    def unlink(self):
        self._check_protected()
        if not self._is_security_admin():
            raise AccessError(
                _("Only Security Administrators may delete users.")
            )
        return super().unlink()
