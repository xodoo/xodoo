# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import random


class default_wizard(models.TransientModel):
    _name = 'default.wizard'
    _description = '配置工具'

    def button_default(self):
        # query = "INSERT INTO res_partner(name,tz) VALUES ('张三','zh_CN')  RETURNING id"
        # self._cr.execute(query)
        # id = self._cr.fetchone()[0]
        #
        # query = "INSERT INTO res_partner( name,parent_id) VALUES ('张三',%s)"  % id
        # self._cr.execute(query)

        # obj = self.env['res.users'].search([('id', '>', 5)])

        # action_id = self.env.ref('cdc.action_company_product_device').id
        # for line in obj:
        #     values = {
        #         # 'action_id': action_id,
        #         'lang': 'zh_CN',
        #         'tz': 'Asia/Shanghai',
        #         'notification_type': 'inbox',
        #     }
        #     line.sudo().write(values)
        #
        #
        # product = self.env['product.product'].search([])
        # for line in product:
        #     values = {
        #         'company_id': False,
        #     }
        #     line.sudo().write(values)

        self.button_default_values()

        return True

    # 消息颜色配置
    def button_default_values(self):

        icon_bg = "'bg-primary', '主色:通常用于品牌颜色'"
        icon_bg = "'bg-secondary', '次色'"
        icon_bg = "'bg-success', '成功:通常是绿色'"
        icon_bg = "'bg-danger', '红色:危险操作的颜色'"
        icon_bg = "'bg-warning', '警告:通常是橙色'"
        icon_bg = "'bg-info', '蓝色:信息'"
        icon_bg = "'bg-light', '浅蓝色'"
        icon_bg = "'bg-dark', '黑色'"

        message_style = []
        values = {
            'name': '讨论',
            'res_model': '',
            'icon': 'fa fa-lg fa-users',  # 对应的图标
            'icon_bg': 'bg-primary',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        message_style.append(values)
        values = {
            'name': '活动',
            'res_model': '',
            'icon': 'fa fa-lg fa-check-circle',  # 对应的图标
            'icon_bg': 'bg-success',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        message_style.append(values)
        values = {
            'name': '注释',
            'res_model': '',
            'icon': 'fa fa-lg fa-info-circle',  # 对应的图标
            'icon_bg': 'bg-warning',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        message_style.append(values)

        values = {
            'name': '销售',
            'res_model': 'sale.order',
            'icon': 'fa fa-lg fa-shopping-cart',  # 对应的图标
            'icon_bg': 'bg-success',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        message_style.append(values)

        values = {
            'name': '采购',
            'res_model': 'purchase.order',
            'icon': 'fa fa-lg fa-shopping-cart',  # 对应的图标
            'icon_bg': 'bg-primary',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        message_style.append(values)

        values = {
            'name': '采购',
            'res_model': 'purchase.order',
            'icon': 'fa fa-lg fa-shopping-cart',  # 对应的图标
            'icon_bg': 'bg-primary',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        values = {
            'name': '会计',
            'res_model': 'account.move',
            'icon': 'fa fa-lg fa-money',  # 对应的图标
            'icon_bg': 'bg-danger',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        message_style.append(values)
        values = {
            'name': '仓库',
            'res_model': 'stock.picking',
            'icon': 'fa fa-lg fa-truck',  # 对应的图标
            'icon_bg': 'bg-info',  # 上面根据重要性选一个色
            'icon_color': '#8e8e90',  # 图标:字体颜色
            'icon_background': '#ffffff',  # 图标:字体背景
            'title_color': '#8e8e90',  # 标题:字体颜色
            'title_background': '#ffffff',  # 标题:字体背景
            'content_color': '#8e8e90',  # 正文:字体颜色
            'content_background': '#ffffff',  # 正文:字体背景
        }
        message_style.append(values)

        for x in message_style:
            domain = []
            if x['res_model']:
                domain = [('res_model', '=', x.get('res_model'))]
            else:
                domain = [('name', '=', x.get('name'))]
                # domain = [('name', '=', x.get('name')),('res_model', '=', x.get('res_model'))]
            message = self.env['mail.message.subtype'].search(domain, order="id desc")
            if message:
                for line in message:
                    if not line.icon:
                        values = {
                            'icon': x.get('icon'),  # 对应的图标
                            'icon_bg': x.get('icon_bg'),  # 上面根据重要性选一个色
                            'icon_color': x.get('icon_color'),  # 图标:字体颜色
                            'icon_background': x.get('icon_background'),  # 图标:字体背景
                            'title_color': x.get('title_color'),  # 标题:字体颜色
                            'title_background': x.get('title_background'),  # 标题:字体背景
                            'content_color': x.get('content_color'),  # 正文:字体颜色
                            'content_background': x.get('content_background'),  # 正文:字体背景
                        }
                        line.write(values)

        self._modify_website()


    def _modify_website(self):
        """替换所有网址与署名"""
        domain=[]
        modules = self.env['ir.module.module'].search(domain, order="id desc")
        for module in modules:
            values = {
                'author': 'Xodoo',
                'website': 'http://www.xodoo.cn',
            }
            module.sudo().write(values)


        user = self.env['res.users'].browse(1)
        values = {
            'name': '机器人',
        }
        user.sudo().write(values)

        domain=[]
        channels = self.env['discuss.channel'].search(domain, order="id desc")
        for channel in channels:
            name = channel.name.replace('OdooBot','机器人')
            values = {
                'name': name,
            }
            channel.sudo().write(values)

        domain=[]
        messages = self.env['mail.message'].search(domain, order="id desc")
        for message in messages:
            email_from = message.email_from.replace('odoobot','机器人')
            email_from = email_from.replace('OdooBot','机器人')
            body = message.body.replace('OdooBot','机器人')
            body = body.replace('Odoo','机器人')
            reply_to = message.reply_to.replace('odoobot','机器人')
            values = {
                'email_from': email_from,
                'body': body,
                'reply_to': reply_to,
            }
            message.sudo().write(values)
        domain=[]
        messages = self.env['res.groups'].search(domain, order="id desc")
        for message in messages:
            name = message.name.replace('Odoo','机器人')
            values = {
                'name': name,
            }
            message.sudo().write(values)




