# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud4
# QQ:35350428
# 邮件:35350428@qq.com
# 手机：13584935775
# 作者：'amos'
# 公司网址： www.odoo.pw  www.xodoo.cn
# Copyright 昆山一百计算机有限公司 2012-2025 Amos
# 日期：2025/1/15
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import xodoo
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare
from werkzeug.urls import url_encode

import xodoo

class amos_test(models.Model):
    _name = "amos.test"
    _description = "测试"


    name = fields.Char('名称')
    user_id = fields.Many2one('res.users')
    title_ids = fields.Many2many('res.partner.title', 'amos_test_res_partner_title_rel', 'test_id', 'title_id')


    def _menu_badge_count(self):
        domain = []
        rows_count = self.sudo().search_count(domain)
        menu_badge = '<span class="badge bg-warning rounded-pill badge-soft-danger text-white float-end">%s</span>' % rows_count
        return menu_badge



    def button_ok(self):

        print(xodoo.get("key1"))  # 输出: value1



        return True



