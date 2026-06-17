{
    "name": "Secure File Upload Enforcement",
    "version": "18.0.1.0.0",
    "category": "Security",
    "summary": "Secure validation layer over ir.attachment uploads",
    "depends": ["base", "web", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/upload_audit_views.xml",
        "data/config_defaults.xml",
    ],
    "installable": True,
    "application": False,
    'external_dependencies': {
        'python': ['python-magic'],
    },
}