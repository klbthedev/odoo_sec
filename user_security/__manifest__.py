{
    "name": "User Security",
    "version": "18.0.2.0.0",
    "summary": "Delegate management of users, groups, ACLs, record rules and other "
               "security-sensitive configuration to a dedicated Security Administrator role.",
    "description": """
User Security
=============

Introduces a dedicated *Security Administrator* role and locks down the
security-sensitive parts of Odoo so that only that role (or a superuser /
automated flow) can modify them:

* users, groups, access control lists (``ir.model.access``) and record rules
* menus, views, fields, actions, scheduled actions (cron)
* system parameters and module installation

The built-in Administrator account and the superuser are flagged as
*protected* and can only be altered by a Security Administrator.
""",
    "website": "",
    "category": "Administration",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "security/menu_security.xml",
        "views/res_users_views.xml",
    ],
    "installable": True,
    "application": False,
}
