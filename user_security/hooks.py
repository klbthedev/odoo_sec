from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    admin_user = env.ref('base.user_admin')
    security_group = env.ref('user_security.group_security_admin')

    admin_user.write({
        'groups_id': [(4, security_group.id)]
    })