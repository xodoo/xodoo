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

import odoo
import odoo.modules.registry
from odoo import http
from odoo.http import content_disposition, request, \
    serialize_exception as _serialize_exception
import json
import uuid

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


class ding(http.Controller):

    @http.route('/web/webclient/print', type='json', auth="user")
    def web_webclient_print(self, **kwargs):
        uid = request.env.user.id
        if kwargs['title'] == '恭喜':
            request.env.user.notify_success(kwargs['message'] + kwargs['date'], kwargs['title'])
        if kwargs['title'] == '失败':
            request.env.user.notify_warning(kwargs['message'] + kwargs['date'], kwargs['title'])
        return True


    @http.route('/xodoo/print', type='json', auth="none", sitemap=False, csrf=False, cors="*")
    def xodoo_print(self, **kw):
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        report = pool['ir.actions.report'].sudo().browse(int(kw['report_id']))

        user =pool['res.users'].sudo().browse(context.get('uid'))

        #默认打印本地服务
        print_url = user.print_url or 'http://127.0.0.1:9090/xodoo/print'
        is_network_printing = 'no'
        if user.print_url:
            is_network_printing = 'yes'

        amos_report_templates = ''
        if report.amos_report_templates:
            amos_report_templates = report.amos_report_templates.strip()
        data = {
            'file_name': str(uuid.uuid4()),
            'name': report.name,
            'data_url': report.data_url,
            'data_url_params': report.data_url_params,
            'print_url': print_url,
            'report_name': report.report_name,
            'client': report.client,
            'amos_type': report.amos_type,
            'model': report.model,
            'is_network_printing': is_network_printing,
            'amos_report_templates': amos_report_templates
        }

        context = dict(request.env.context)
        print(kw)
        print(context)
        docids = kw.get('context').get('active_ids')
        if report.report_type == 'html':
            html = report.with_context(context)._render_qweb_html(report.report_name,docids, data=None)[0]
        elif report.report_type == 'qweb-html':
            html = report.with_context(context)._render_qweb_html(report.report_name,docids, data=None)[0]
        elif report.report_type == 'qweb-grf':
            html = report.with_context(context)._render_qweb_html_grf(report.report_name,docids, data=None)[0]
        elif report.report_type == 'text':
            html = report.with_context(context)._render_qweb_text(report.report_name,docids, data=None)[0]

        data['report_data'] = html.decode().strip()

        return json.dumps(data)