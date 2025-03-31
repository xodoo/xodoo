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


{
    'name': '系统底层',
    'summary': '官方网站',
    'category': '中台应用/底层',
    'sequence': 0,
    'author': 'Amos',
    'website': 'http://www.opensn.cn',
    'depends': ['base', 'web','mail','http_routing'],
    'version': '0.1',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/mail_message_subtype.xml',
        'data/ir_config_parameter.xml',

        'wizard/default_wizard.xml',

        'views/http_routing_template.xml',
        'views/res_config_settings_views.xml',
        'views/base_views.xml',
        'views/mail_message_subtype.xml',
        'views/mail_activity_type.xml',
        'views/mail_activity.xml',
        'views/mail_message.xml',
        'views/xodoo_res_partner.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
""",
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'xodoo/static/src/css/xodoo_form.css',
            'xodoo/static/src/css/tree.css',
            'xodoo/static/src/css/required_field_underline.css',
            'xodoo/static/src/scss/sheet.css',

            # 'xodoo/static/src/zTreeStyle/zTreeStyle.css',
            # 'xodoo/static/src/js/echarts.min.js',
            # 'xodoo/static/src/js/jquery.ztree.core.js',
            # 'xodoo/static/src/js/jquery.ztree.excheck.js',
            # 'xodoo/static/src/js/jquery.ztree.exedit.js',
            # 'xodoo/static/src/js/jquery.ztree.exhide.js',
            # 'xodoo/static/src/js/fuzzysearch.js',

        ],

    },

}
