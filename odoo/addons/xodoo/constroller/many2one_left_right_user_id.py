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

import json
import os
import odoo
from odoo import http, fields, _
from odoo.http import request
from jinja2 import Environment, FileSystemLoader
from odoo.tools.image import image_data_uri, binary_to_image
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo import http,api, fields, models, tools, SUPERUSER_ID, _



BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/templates")
env = Environment(loader=templateLoader)
import logging
_logger = logging.getLogger(__name__)

# TODO(amos): 提供更多格式化方法
env.filters['image_data_uri'] = image_data_uri

class many2one_left_right_user_id(http.Controller):

    @http.route(['/xodoo/many2one_left_right_user_id'], type='http', auth="public", csrf=False)
    def xodoo_many2one_left_right_user_id(self, **kw):
        """
        用户选择
        :param post:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        values = {}
        list = self.get_ztree_hr_department(kw)
        values['zNodes'] = json.dumps(list)

        print(list)
        template = env.get_template('many2one/left_right/hr_department.html')
        html = template.render(object=values)
        return html


    def get_ztree_hr_department(self,kw):
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env

        print(kw)

        obj = pool[kw.get('fun_model')].sudo().search([('parent_id', '=', False)])
        list = []
        for line in obj:
            v = {
                # "sequence": line.sequence,
                "id": line.id,
                "pId": 0,
                "name": line.name,
                "open": False,
            }
            list.append(v)

            if len(line.child_ids) > 0:
                list = self.get_tree_next(list, line, line.id)
        return list

    def get_tree_next(self, list, obj, pid):
        for line in obj.child_ids:
            v = {
                # "sequence": line.sequence,
                "id": line.id,
                "pId": pid,
                "name": line.name,
                "open": False,
            }
            list.append(v)
            if len(line.child_ids) > 0:
                self.get_tree_next(list, line, line.id)
        return list

