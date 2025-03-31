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
import ast


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/templates")
env = Environment(loader=templateLoader)
import logging
_logger = logging.getLogger(__name__)

# TODO(amos): 提供更多格式化方法
env.filters['image_data_uri'] = image_data_uri

class print_web(http.Controller):

    @http.route('/xodoo/index', type='http', auth="public", csrf=False)
    def xodoo_index(self, **post):
        """
        地图
        :param post:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        values = {}
        values['user'] = pool.user

        template = env.get_template('index.html')
        html = template.render(object=values)
        return html

    @http.route('/xodoo/easyui', type='http', auth="public", csrf=False)
    def xodoo_layui(self, **kw):
        """
        地图
        :param post:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        values = {}
        values['user'] = pool.user
        values['o'] = kw
        # obj = pool[kw.get('fun_model')]

        template = env.get_template('layui.html')
        html = template.render(object=values)
        return html



    @http.route(['/xodoo/easyui/data'], type='json', auth="public", cors="*", csrf=False)
    def xodoo_layui_data(self, **kw):
        """
        地图
        :param post:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        values = {}
        params = request.httprequest.json
        values['user'] = pool.user
        values['o'] = params

        obj = pool[params.get('fun_model')]
        limit = int(params.get('page_size'))  # 每页显示数量
        offset = limit * (int(params.get('page')) - 1)  # 查询数据库记录
        domain = self._get_search_domain(params) #查询条件

        all_search_count = obj.sudo().search_count(domain)
        fun_field = params.get('fun_field').split(',')
        datas = obj.sudo().search_read(domain,fun_field, limit=limit, offset=offset, order=self._get_search_order(kw))
        for o in datas:
            for key, value in o.items():
                type = obj._fields[key].type
                if type in ('char', 'text', 'selection','html'):
                    o[key] = value
                elif type == 'float':
                    pass
                elif type == 'boolean':
                    pass
                elif type == 'integer':
                    o[key] = value
                elif type == 'binary':
                    o[key] = value
                elif type == 'many2one':
                    if value:
                        o[key] = "%s,%s" % (value[0],value[1])
                    else:
                        o[key] = ""
                elif type == 'many2many':

                    if value:
                        o[key] = "%s,%s" % (value[0],value[1])
                    else:
                        o[key] = ""
                elif type == 'datetime':
                    o[key] = tools.jinja_filters.date_filter(value, 0, 19)  # 创建时间
                elif type == 'date':
                    if value:
                        o[key] = tools.jinja_filters.date_filter(value, 0, 10)
                    else:
                        o[key] = ""


        if request.httprequest.method == 'POST':
            pass
        else:
            pass

        # self.all_count = all_count  # 总数
        # self.limit = limit  # 每页显示数据
        # self.page = page  # 当前要显示的页码
        # self.show_page_count = show_page_count  # 显示分页数量

        # ::::::字段列表
        cols = ""
        fields = params.get('fun_field')
        if fields:
            cols_field = []
            # 选择
            j = {
                "type": 'checkbox',
                "fixed": 'left',
            }
            cols_field.append(j)


            for f in fields.split(','):
                title = obj.fields_get([f]).get(f).get('string')
                j = {
                    "field": f,
                    "title": title,
                    "width": 80,
                }

                type = obj._fields[f].type
                if type in ('char', 'text', 'selection','html'):
                    j['width'] = params.get('fun_field_width').get(f,80)
                    j['sort'] = 'true'
                elif type == 'float':
                    pass
                elif type == 'boolean':
                    pass
                elif type == 'integer':
                    j['width'] = params.get('fun_field_width').get(f,80)
                    j['sort'] = 'true'
                elif type == 'binary':
                    pass
                elif type == 'many2one':
                    pass
                elif type == 'datetime':
                    j['width'] = params.get('fun_field_width').get(f,80)
                    j['sort'] = 'true'
                elif type == 'date':
                    pass
                cols_field.append(j)

            cols = [cols_field]


        else:
            pass

        values = {
            "errcode": 0,  # 错误码
            "cols": cols,
            "errmsg": "ok",
            "all_search_count": all_search_count,
            "data": datas,
            "message": "请求成功！",
        }
        return json.dumps(values ,cls=tools.jinja_filters.DateEncoder)

    def _get_search_domain(self, params):
        search_name = params.get('search_name', '').strip()
        search_startDate = params.get('search_startDate', '')
        search_endDate = params.get('search_endDate', '')
        domain = []
        if params.get('domain'):
            domain = ast.literal_eval(params['domain']) if params['domain'] is not None else kw['domain']

        if search_name:
            for srch in search_name.split(" "):
                domain += [('name', 'ilike', srch)]

        if search_startDate:
            domain += [('create_date', '>=', search_startDate)]

        if search_endDate:
            domain += [('create_date', '<=', search_endDate)]

        return domain


    def _get_search_order(self, post):
        return 'id desc,%s , id desc' % post.get('order', 'id desc')

    @http.route('/xodoo/many2one', type='http', auth="public", csrf=False)
    def xodoo_many2one(self, **kw):
        """
        many2one 默认界面
        :param post:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        values = {}
        values['user'] = pool.user
        values['o'] = kw
        # obj = pool[kw.get('fun_model')]

        template = env.get_template('many2one/index.html')
        html = template.render(object=values)
        return html