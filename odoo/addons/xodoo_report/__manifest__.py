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

{
    'name': '报表协议',
    'summary': '支持锐浪,Xodoo浏览器,指挥平台,NET4客户端',
    'category': '企业应用/报表',
    'sequence': 20000,
    'author': 'Amos',
    'website': 'http://www.xodoo.cn',
    'depends': ['base', 'web'],
    'version': '0.1',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'view/ir_actions_report_xml_view.xml',
        'view/res_users_view.xml',
        'view/res_printer_view.xml',
        'view/ir_model.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
        ],
    },
    'description': """
报表相关底层修改
/odoo/tools/convert.py
def _tag_report(self, rec, data_node=None, mode=None):
增加前端字端

odoo/addons/web/static/src/webclient/actions/action_service.js
js _executeReportClientAction

使用网络打印时要求是公网IP
""",
}
