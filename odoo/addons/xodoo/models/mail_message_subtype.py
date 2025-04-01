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
import xodoo
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.osv import expression


class mail_message_subtype(models.Model):
    _inherit = 'mail.message.subtype'

    icon = fields.Char(string='图标', default=lambda self: 'fa fa-lg fa-cog')

    form_id = fields.Integer(string='表单', default=0)
    tree_id = fields.Integer(string='列表', default=0)


    icon_bg = fields.Selection([
        ('bg-primary', '主色:通常用于品牌颜色'),
        ('bg-secondary', '次色'),
        ('bg-success', '成功:通常是绿色'),
        ('bg-danger', '红色:危险操作的颜色'),
        ('bg-warning', '警告:通常是橙色'),
        ('bg-info', '蓝色:信息'),
        ('bg-light', '浅蓝色'),
        ('bg-dark', '黑色'),
    ], string='图标背景', default='bg-primary')

    # @api.model
    # def _default_style_json(self):
    #
    #     values = {
    #         'icon_color': 'bg-primary',#图标:字体颜色
    #         'icon_background': '#8e8e90',#图标:字体颜色
    #         'title_color': '#8e8e90',#标题:字体颜色
    #         'title_background': '#ffffff',#标题:字体背景
    #         'content_color': '#8e8e90',#正文:字体颜色
    #         'content_background': '#ffffff',#正文:字体背景
    #     }
    #     return values
    #
    # style_json = fields.Json(string='部件', default=_default_style_json)
    #


    icon_color = fields.Char(string='图标:字体颜色', default='#8e8e90')
    icon_background = fields.Char(string='图标:字体背景', default='#ffffff')

    title_color = fields.Char(string='标题:字体颜色', default='#8e8e90')
    title_background = fields.Char(string='标题:字体背景', default='#ffffff')

    content_color = fields.Char(string='正文:字体颜色', default='#8e8e90')
    content_background = fields.Char(string='正文:字体背景', default='#ffffff')

    def button_icon_bg(self):
        context = dict(self._context or {})
        self.icon_bg = context.get('icon_bg')
        return True


