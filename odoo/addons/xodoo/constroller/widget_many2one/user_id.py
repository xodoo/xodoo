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
print(BASE_DIR)
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/templates")
env = Environment(loader=templateLoader)
import logging
_logger = logging.getLogger(__name__)

# TODO(amos): 提供更多格式化方法
env.filters['image_data_uri'] = image_data_uri

class print_web(http.Controller):

    @http.route(['/xodoo/many2one/user_id'], type='http', auth="public", csrf=False)
    def xodoo_many2one_user_id(self):
        """
        人员
        :param post:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        values = {}
        values['user'] = pool.user

        cids = request.httprequest.cookies.get('cids')
        if cids:
            allowed_company_ids = {int(cid) for cid in cids.split(',')}
        else:
            allowed_company_ids = {request.env.company.id}

        company = pool['res.company'].sudo().search([('id', 'in', tuple(allowed_company_ids))])
        values['company'] = company
        # 默认集团总部 递归重复查询 id != parent_id 结束条件
        obj = pool['hr.department'].sudo().search([('company_id', '=', company[0].id), ('parent_id', '=', False)])
        list = []
        for line in obj:
            # 父结点
            v = {
                "id": line.id,
                "title": line.name,
                "spread": str(True).lower(),
                "children": [],
            }
            list.append(v)
            if len(line.child_ids) > 0:
                list = self.get_demo_next(list, line, line.id)
        values['department'] = list
        template = env.get_template('user_id/index.html')
        # template = env.get_template('many2one/left_right/index.html')
        html = template.render(object=values, company_name=company[0].name)
        return html

    def get_demo_next(self,list,obj,pid):
        for line in obj.child_ids:
            v = {
                "id": line.id,
                "label": line.name,
                "spread": str(True).lower(),
                "children": [],
            }
            list[0]['children'].append(v)
            if len(line.child_ids)>0:
                self.get_demo_next(list[0]['children'], line, line.id)
        return list

    @http.route('/xodoo/user_id/department_id', type='http', auth="public", csrf=False)
    def xodoo_user_id_department_id(self, company_id):
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        values = {}
        obj = pool['hr.department'].sudo().search([('company_id', '=', int(company_id)), ('parent_id', '=', False)], order="id desc")
        list = []
        for line in obj:
            # 父结点
            v = {
                "id": line.id,
                "pid": 0,
                "label": line.name,
                "spread": str(True).lower(),
                "children": [],
            }
            list.append(v)
            if len(line.child_ids) > 0:
                list = self.get_demo_next(list, line, line.id)
        values['department'] = list
        data = {
            "errcode": 0,
            'errmsg': 'ok',
            "data": values,
            'message': '提交成功!'}
        return json.dumps(data)

    @http.route('/xodoo/user_id/staff', type='http', auth="public", csrf=False)
    def xodoo_demo_staff(self, treedata, input):
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        treedata = json.loads(treedata)
        list_id = []
        if treedata:
            for k, w in treedata.items():
                if k == 'id':
                    list_id.append(w)
                if k == 'children' and w:
                    list_id = self.get_id_employee(list_id, w)

        list = []
        for i in list_id:
            employee = pool['hr.employee'].sudo().search([('department_id', '=', i)])
            for j in employee:
                v = {
                    "name": j.name,
                    "id": j.id,
                    "department": j.department_id.name,
                    "company": j.company_id.name,
                }
                list.append(v)
        # 筛选员工列表 4 -1  -1
        for line in range(len(list) - 1, -1, -1):
            if input not in list[line]['name']:
                list.pop(line)

        return json.dumps(list)

    def get_id_employee(self, list, son):
        if len(son) > 0:
            for i in range(len(son)):
                for k, w in son[i].items():
                    if k == 'id':
                        list.append(w)
                    if k == 'children' and w:
                        self.get_id_employee(list, w)
        return list

