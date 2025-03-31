# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# odoo18
# QQ:35350428
# 邮件:35350428@qq.com
# 手机：13584935775
# 作者：'Amos'
# 公司网址： www.xodoo.cn
# Copyright 昆山一百计算机有限公司
# 日期：2025-01-01
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import uuid
from itertools import groupby
from datetime import datetime, timedelta
from werkzeug.urls import url_encode
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.osv import expression


class mail_activity_type(models.Model):
    _inherit = 'mail.activity.type'



    is_dashboard = fields.Boolean(default=True, string='是否工作台显示')


class mail_activity(models.Model):
    _inherit = 'mail.activity'
    _rec_name = 'res_name'
    _order = 'id desc'

    name = fields.Char(string='单据编号', default=lambda self: 'New')



    def button_open(self):
        context = dict(self.env.context or {})
        context['mobile'] = self.partner_id.mobile
        context['ref'] = '%s,%s' % (self._name, self.id)
        context['partner_id'] = self.partner_id.id
        context['name'] = '%s:%s 交货日期:%s,请注意查收!' % (self._description, self.name, self.delivery_date)
        return {
            'name': u'发短信',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ir.message',
            'view_id': self.env.ref('Amos_Base.view_form_message_wizard').id,
            'type': 'ir.actions.act_window',
            'res_id': False,
            'context': context,
            'target': 'new'
        }

