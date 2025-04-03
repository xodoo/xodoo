# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# odoo17
# QQ:35350428
# 邮件:35350428@qq.com
# 手机：13584935775
# 作者：'Amos'
# 公司网址： www.xodoo.cn
# Copyright 昆山一百计算机有限公司
# 日期：2023-09-16
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.osv import expression

class res_company(models.Model):
    _inherit = 'res.company'

    preview = fields.Boolean('是否预览', default=True)
    direct_printing = fields.Boolean('直接打印', default=False)
    printername = fields.Char(string='打印机名称',default='')


