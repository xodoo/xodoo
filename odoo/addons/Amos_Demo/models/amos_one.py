# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Odoo Connector
# QQ:35350428
# 邮件:sale@100china.cn
# 手机：13584935775
# 作者：amos
# 公司网址： www.odoo.pw  www.100china.cn
# Copyright 昆山一百计算机有限公司 2012-2019 Amos
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare
from werkzeug.urls import url_encode
from collections import defaultdict
from odoo.tools.safe_eval import safe_eval, test_python_expr


class amos_one(models.Model):
    _name = "amos.one"
    _description = "第一"
    _inherit = ['mail.thread']

    name = fields.Char(string='名称', required=True, default=lambda self: '测试一')
    one_ids = fields.One2many('amos.one.line', 'one_id', string='明细行', copy=True, auto_join=True)
    product_uom_qty = fields.Float(string='数量', required=True, default=1.0)
    state = fields.Selection([
        ('新建', '新建'),
        ('校对', '校对'),
        ('审核', '审核'),
        ('批准', '批准'),
        ('已发布', '已发布'),
    ], string='状态', readonly=True, copy=False, index=True, tracking=True,
        default='新建')

    @api.model
    def _verify_workflow(self, test=1):
        """
        test 执行次数
        """
        print('----')
        return True


class amos_one_line(models.Model):
    _name = "amos.one.line"
    _description = "第一明细"

    one_id = fields.Many2one('amos.one', string='明细', required=True, ondelete='cascade', index=True, copy=False)
    name = fields.Char(string='名称', required=True, default=lambda self: '测试')
