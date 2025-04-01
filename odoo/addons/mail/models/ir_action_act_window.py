# -*- coding: utf-8 -*-
from odoo import fields, models
import xodoo


class ActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(selection_add=[
        ('activity', 'Activity')
    ], ondelete={'activity': 'cascade'})
