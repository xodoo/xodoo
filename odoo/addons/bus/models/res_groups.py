# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
import xodoo


class ResGroups(models.Model):
    _name = "res.groups"
    _inherit = ["res.groups", "bus.listener.mixin"]
