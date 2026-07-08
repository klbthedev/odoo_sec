from odoo import models


# --- Actions (privilege-escalation vectors: server actions, crons, ...) -------

class IrActionsActWindow(models.Model):
    _name = "ir.actions.act_window"
    _inherit = ["ir.actions.act_window", "security.guarded.mixin"]


class IrActionsServer(models.Model):
    _name = "ir.actions.server"
    _inherit = ["ir.actions.server", "security.guarded.mixin"]


class IrActionsClient(models.Model):
    _name = "ir.actions.client"
    _inherit = ["ir.actions.client", "security.guarded.mixin"]


class IrActionsReport(models.Model):
    _name = "ir.actions.report"
    _inherit = ["ir.actions.report", "security.guarded.mixin"]


class IrActionsActUrl(models.Model):
    _name = "ir.actions.act_url"
    _inherit = ["ir.actions.act_url", "security.guarded.mixin"]


# --- UI / metadata ------------------------------------------------------------

class IrUiView(models.Model):
    _name = "ir.ui.view"
    _inherit = ["ir.ui.view", "security.guarded.mixin"]


class IrModelFields(models.Model):
    _name = "ir.model.fields"
    _inherit = ["ir.model.fields", "security.guarded.mixin"]


# --- System configuration -----------------------------------------------------

class IrCron(models.Model):
    _name = "ir.cron"
    _inherit = ["ir.cron", "security.guarded.mixin"]


class IrConfigParameter(models.Model):
    _name = "ir.config_parameter"
    _inherit = ["ir.config_parameter", "security.guarded.mixin"]


class IrModuleModule(models.Model):
    _name = "ir.module.module"
    _inherit = ["ir.module.module", "security.guarded.mixin"]