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

{
    'name': 'xodoo 基本功能教学',
    'version': '1.0',
    'category': '中台应用/教学',
    'summary': '功能说明',
    'sequence': 0,
    'author': 'Amos',
    'website': 'http://xodoo.cn',
    'license': 'LGPL-3',
    'depends': ['mail','xodoo'],
    'data': [
        'data/amos_demo_tag_data.xml',
        'security/ir.model.access.csv',
        # 'data/amos_demo_data.xml',
        'views/menuitem.xml',
        'views/amos_demo1.xml',
        # 'views/amos_demo2.xml',
        # 'views/amos_demo3.xml',
        # 'report/report.xml',
        'views/amos_one.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    odoo 基本功能教学
    """,
}
