# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import time
import base64
import io
import logging
import json
from odoo.tools import check_barcode_encoding, config, is_html_empty, parse_version

_logger = logging.getLogger(__name__)

amos_type = [
    ('xls', '导出Excel'),
    ('txt', '导出TXT'),
    ('htm', '导出HTML'),
    ('rtf', '导出RTF'),
    ('pdf', '导出PDF'),
    ('csv', '导出CSV'),
    ('tif', '导出Image'),
    ('print', '直接打印'),
    ('zpl', 'zpl指令打印'),
    ('grf', 'grf'),
]


class res_print_data(models.Model):
    _name = 'res.print.data'
    _description = '打印数据'

    name = fields.Char('关联')
    data = fields.Text('数据')
    user_id = fields.Many2one('res.users', string='打印人')


class ir_actions_actions(models.Model):
    _inherit = 'ir.actions.actions'

    amos_type = fields.Selection(amos_type, string='输出方式')
    amos_report_templates = fields.Text('报表模板代码')
    attachment_id = fields.Many2one('ir.attachment', string='报表模板', ondelete='cascade')
    client = fields.Selection([
        ('rubylong', '官方客户端'),
        ('browser', 'AmosERP专用浏览器'),
        ('net4_client', 'Net4客户端'),
        ('ABNCP', '指挥平台'),
    ], string='类型')



    @api.onchange('amos_report_templates')
    def onchange_amos_report_templates(self):
        """
        如果明细有变化就更新附件
        :return:
        """
        if self.amos_report_templates:

            if self.attachment_id:
                self.write({'datas': base64.b64encode(bytes(self.amos_report_templates, encoding="utf-8"))})
            else:
                attachment = self.env['ir.attachment'].create({
                    'datas': base64.b64encode(bytes(self.amos_report_templates, encoding="utf-8")),
                    'name': self.name,
                }
                )
                self.write({'attachment_id': attachment.id})


class ir_actions_Report(models.Model):
    _inherit = 'ir.actions.report'


    report_type = fields.Selection(selection_add=[('qweb-grf','XODOO')], ondelete={'qweb-grf': 'cascade'})

    data_url = fields.Char(string='数据URL', default=lambda self: '',help='支持URL动态请求')
    data_url_params = fields.Text('参数',default='',help='支持URL动态请求')



    def _get_rendering_context(self, report, docids, data):
        # access the report details with sudo() but evaluation context as current user

        # If the report is using a custom model to render its html, we must use it.
        # Otherwise, fallback on the generic html rendering.
        report_model = self._get_rendering_context_model(report)


        data = data and dict(data) or {}

        if report_model is not None:
            data.update(report_model._get_report_values(docids, data=data))
        else:
            url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

            context = dict(self._context or {})
            context['lang'] = self.env.user.lang
            context['amos'] = 'amos-amos'

            docs = self.env[report.model].browse(docids)
            data.update({
                'doc_ids': docids,
                'doc_model': report.model,
                'docs': docs,
                'report': self,
                'report_url': url,
                'context': context,
                'amos_type': self.amos_type,
                'client': self.client,
                'amos_report_templates': self.amos_report_templates,
            })
        return data

    def _get_rendering_context_model(self, report):
        report_model_name = 'report.%s' % report.report_name
        return self.env.get(report_model_name)


    def _get_rendering_context_grf(self, report, docids, data):
        # If the report is using a custom model to render its html, we must use it.
        # Otherwise, fallback on the generic html rendering.
        report_model = self._get_rendering_context_model(report)

        data = data and dict(data) or {}

        if report_model is not None:
            data.update(report_model._get_report_values(docids, data=data))
        else:
            docs = self.env[report.model].browse(docids)
            data.update({
                'doc_ids': docids,
                'doc_model': report.model,
                'docs': docs,
            })
            if self.amos_type != False:
                url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                context = dict(self._context or {})
                context['lang'] = self.env.user.lang
                context['amos'] = 'amos-amos'

                data.update({
                    'report': self,
                    'report_url': url,
                    'context': context,
                    'amos_type': self.amos_type,
                    'client': self.client,
                    'amos_report_templates': self.amos_report_templates,
                })

                return data
        data['is_html_empty'] = is_html_empty
        return data


    @api.model
    def _render_qweb_html_grf(self,report_ref, docids, data=None):


        if not data:
            data = {}
        data.setdefault('report_type', 'html')
        report = self._get_report(report_ref)
        data = self._get_rendering_context_grf(report, docids, data)
        return self._render_template(report.report_name, data), 'html'



    def get_grf(self,name):
        obj = self.search([('report_name', '=', name)], limit=1)

        values = {
            'model': obj.model,
            'report_id': obj.id,
            'report_type': obj.amos_type,
            'amos_report_templates': obj.amos_report_templates,
        }

        return values


    def download_template(self):
        """ 判断报表模板并生成附件，用户点下载 """
        for report in self:
            if report.attachment_id:
                report.write({'db_datas': base64.b64encode(bytes(report.amos_report_templates, encoding="utf-8"))})
            else:
                attachment = self.env['ir.attachment'].create({
                    'db_datas': base64.b64encode(bytes(report.amos_report_templates, encoding="utf-8")),
                    'name': report.name,
                    # 'datas_fname': '%s.grf' % report.name
                })
                report.write({'attachment_id': attachment.id})
        return True


    def report_action(self, docids, data=None, config=True):
        """Return an action of type ir.actions.report.

        :param docids: id/ids/browse record of the records to print (if not used, pass an empty list)
        :param report_name: Name of the template to generate an action for
        """

        context = self.env.context
        if docids:
            if isinstance(docids, models.Model):
                active_ids = docids.ids
            elif isinstance(docids, int):
                active_ids = [docids]
            elif isinstance(docids, list):
                active_ids = docids
            context = dict(self.env.context, active_ids=active_ids)

        report_action = {
            'context': context,
            'data': data,
            'type': 'ir.actions.report',
            'report_name': self.report_name,
            'report_type': self.report_type,
            'report_file': self.report_file,
            'name': self.name,
            'amos_type': self.amos_type,
            'client': self.client,
            'amos_report_templates': self.amos_report_templates,
        }

        discard_logo_check = self.env.context.get('discard_logo_check')
        if self.env.is_admin() and not self.env.company.external_report_layout_id and config and not discard_logo_check:
            action = self.env["ir.actions.actions"]._for_xml_id("web.action_base_document_layout_configurator")
            ctx = action.get('context')
            py_ctx = json.loads(ctx) if ctx else {}
            report_action['close_on_report_download'] = True
            py_ctx['report_action'] = report_action
            action['context'] = py_ctx
            return action

        return report_action

