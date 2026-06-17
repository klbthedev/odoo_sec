from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    login_lockout_max_attempts = fields.Integer(
        string="Maximum Failed Login Attempts",
        config_parameter="auth_login_lockout.login_lockout_max_attempts",
        default=5,
    )

    login_lockout_duration = fields.Integer(
        string="Lock Duration (Minutes)",
        config_parameter="auth_login_lockout.login_lockout_duration",
        default=15,
    )
    login_lockout_max_lockouts = fields.Integer(
        string="Maximum Lockouts Before Permanent Block",
        config_parameter="auth_login_lockout.login_lockout_max_lockouts",
        default=3,
    )

    login_lockout_exclude_admins = fields.Boolean(
        string="Exclude Internal Administrators",
        config_parameter="auth_login_lockout.login_lockout_exclude_admins",
        # default=True,
    )
