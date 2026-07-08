from odoo import models


# --- Actions (privilege-escalation vectors: server actions, crons, ...) -------

class IrActionsActWindow(models.Model):
    _inherit = ["ir.actions.act_window", "security.guarded.mixin"]


class IrActionsServer(models.Model):
    _inherit = ["ir.actions.server", "security.guarded.mixin"]


class IrActionsClient(models.Model):
    _inherit = ["ir.actions.client", "security.guarded.mixin"]


class IrActionsReport(models.Model):
    _inherit = ["ir.actions.report", "security.guarded.mixin"]


class IrActionsActUrl(models.Model):
    _inherit = ["ir.actions.act_url", "security.guarded.mixin"]


# --- UI / metadata ------------------------------------------------------------

class IrUiView(models.Model):
    _inherit = ["ir.ui.view", "security.guarded.mixin"]


class IrModelFields(models.Model):
    _inherit = ["ir.model.fields", "security.guarded.mixin"]


# --- System configuration -----------------------------------------------------

class IrCron(models.Model):
    _inherit = ["ir.cron", "security.guarded.mixin"]


class IrConfigParameter(models.Model):
    _inherit = ["ir.config_parameter", "security.guarded.mixin"]


class IrModuleModule(models.Model):
    _inherit = ["ir.module.module", "security.guarded.mixin"]
