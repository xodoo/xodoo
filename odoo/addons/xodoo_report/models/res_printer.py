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

printer_type = [
    ('xls', '导出Excel'),
    ('txt', '导出TXT'),
    ('htm', '导出HTML'),
    ('rtf', '导出RTF'),
    ('pdf', '导出PDF'),
    ('csv', '导出CSV'),
    ('tif', '导出Image'),
    ('print', '直接打印'),
]

class res_printer(models.Model):
    _name = 'res.printer'
    _description = '打印机管理'

    name = fields.Char(u"打印机名称", default='')
    print_url = fields.Char(string='网络打印地址',default='')
    user_id = fields.Many2one('res.users', string='打印机负责人',tracking=True ,
                                  default=lambda self: self.env.user)
    printer_type = fields.Selection(printer_type, string='输出方式')

    def write(self, vals):
        if self.user_id.id != self._uid and self._uid not in [1,2]:
            raise UserError('警告：只有当前打印负责人才可以修改！')
        return super(res_printer, self).write(vals)


    def unlink(self):
        for order in self:
            if order.user_id.id != self._uid and self._uid not in [1,2]:
                raise UserError('警告：当前打印负责人不是你！')
        return super(res_printer, self).unlink()

