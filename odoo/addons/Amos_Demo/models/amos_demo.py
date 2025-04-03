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

import base64
# from docx2pdf import convert
import os
import subprocess
from datetime import datetime, timedelta, date
import time
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
import uuid
from odoo.tools import date_utils
# import xodoo
from odoo import api, fields, models, _

import xodoo

#::::::::::字段属性
"""
size=50                   长度
translate=False           翻译
required=True                   必填
index=True                      索引
default=fields.Datetime.now()   长日期
string='年度'                    字段中文名称
tracking=True                   启用社交后记录字段历史变更信息
copy=False                      数据被复制时是否同时复制当前字段
readonly=True                   视图字段为只读，不可编辑，但如果在视图中定义属性以视图为准
strip_style=True
"""


class amos_demo_tag(models.Model):
    _name = "amos.demo.tag"
    _description = "演示工作流明细"
    _order = 'id desc'

    name = fields.Char(string='标签')
    color = fields.Integer(string='颜色', default=1)


class amos_demo(models.Model):  # 一般与 _name 同名 点换成下划线
    _name = "amos.demo"  # 表名
    _description = "演示工作流"  # 表的中文名称
    _order = 'id desc'  # 数据排序方式
    _inherit = ['mail.thread', 'mail.activity.mixin']  # 引入社交：可以记录附件，保存历史字段变更信息

    @api.model
    def default_get(self, fields):
        res = super(amos_demo, self).default_get(fields)
        lines = []
        pram = {
            'name': '主要修理内容',
            'state': '新建',
        }
        lines.append((0, 0, pram))
        pram = {
            'name': '主要更换或修复部件',
            'state': '已发布',
        }
        lines.append((0, 0, pram))



        data = {
            'order_line1': lines,
            'tag_ids': [(6, 0, [1,2,3,4,5,6,7,8,9,10])],
        }


        res.update(data)
        return res

    year = fields.Char(string='年度', required=True, index=True, default=lambda self: fields.datetime.now().year)
    month = fields.Char(string='月度', required=True, index=True, default=lambda self: fields.datetime.now().month)
    hour = fields.Char(string='小时', required=True, index=True, default=lambda self: fields.datetime.now().hour)
    week_start = fields.Char(string='星期几', required=True, default=lambda self: fields.datetime.now().weekday() + 1)
    week = fields.Char(string='在全年多少周', required=True, default=fields.Datetime.now().isocalendar()[1])
    quarter = fields.Char(string='季', required=True,
                          default=lambda self: str(date_utils.get_quarter_number(fields.datetime.now())))
    create_date = fields.Datetime(string='创建时间', required=True, readonly=True, index=True, copy=False,
                                  default=fields.Datetime.now)
    date = fields.Date('截止日期', tracking=True, default=fields.Date.today, required=True)

    top_time = fields.Datetime('置顶', default=fields.Datetime.now())  # 默认当前日期

    @api.onchange('create_date')
    def onchange_create_date(self):
        values = {}
        if self.create_date:
            values['year'] = self.create_date.year
            values['month'] = self.create_date.month
            values['hour'] = self.create_date.hour + 8
            values['week_start'] = self.create_date.weekday() + 1
            values['week'] = self.create_date.isocalendar()[1]
            values['quarter'] = str(date_utils.get_quarter_number(self.create_date))
        self.update(values)

    name = fields.Char(string='项目名称', default='News')
    color = fields.Integer(string='颜色', )
    date_start = fields.Date('客户交期', tracking=True)
    user_id = fields.Many2one('res.users', string='负责人', index=True, tracking=True,
                              default=lambda self: self.env.user, )

    company_id = fields.Many2one('res.company', '公司', required=True, default=lambda s: s.env.company.id, index=True)
    active = fields.Boolean(default=True, string='是否归档', tracking=True)

    tag_ids = fields.Many2many('amos.demo.tag', 'amos_demo_amos_demo_tag_rel', 'demo_id', 'tag_id')

    order_line1 = fields.One2many('amos.demo.line', 'order_id1', string=u'明细行', copy=True)

    note = fields.Text(u'备注', tracking=True)

    sequence = fields.Integer(string='排序', default=50)

    type = fields.Selection([
        ('上架', '上架'),
        ('下架', '下架'),
    ], string='类型', default='上架')

    line_up = fields.Selection([
        ('上海', '上海'),
        ('北京', '北京'),
        ('南京', '南京'),
    ], string='项目城市', default='上海')

    state = fields.Selection([
        ('新建', '新建'),
        ('校对', '校对'),
        ('审核', '审核'),
        ('批准', '批准'),
        ('已发布', '已发布'),
    ], string='状态', readonly=True, copy=False, index=True, tracking=True,
        default='新建')

    name_1 = fields.Char(string='文本', default='文本')
    name_2 = fields.Datetime(string='长日期', default=xodoo.fields.Datetime.now("Asia/Shanghai"))
    name_3 = fields.Date(string='短日期', default=lambda self: xodoo.fields.Date.today())
    name_4 = fields.Image(string='左图片', max_width=50, max_height=50)
    name_5 = fields.Image(string='右图片', max_width=50, max_height=50)

    w_email = fields.Char(string='1,电子邮件', default='35350428@qq.com')
    w_selection = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ], string='2,下拉选择', default='A')

    w_progressbar = fields.Integer(string='3,进度条', default=10)
    w_url = fields.Char(string='4,文本', default='http://xodoo.cn')

    w_radio = fields.Selection([
        ('男', '男'),
        ('女', '女'),
    ], string='5,下拉选择', default='男')

    w_monetary = fields.Float('6,金额', required=True, default=0.0, digits=(10, 2))
    currency_id = fields.Many2one('res.currency')

    a_note = fields.Text(string='大文本',default="""
    俄军指出，阿瓦迪夫卡地下隧道内尚有乌克兰军队的残余部队活动，俄军正在紧密搜索。在攻占火车站过程中，第55摩托化步兵旅特种部队与正试图突破封锁的乌克兰军队遭遇。
    
    """

                         )


    w_hour = fields.Float('7,时间', required=True, default=10.30, digits=(10, 2))

    w_priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High'),
        ('4', 'Very Good'),
        ('5', 'Very Beautiful'),
    ], string='8.星级', index=True,
        default='5')

    w_boolean = fields.Boolean(default=True, string='9,是否', track_visibility='onchange')

    w_note = fields.Text(string='20,编辑')

    w_state_selection = fields.Selection([
        ('成功', '成功'),
        ('失败', '失败'),
    ], string='10,下拉类型', default='成功')

    w_icon = fields.Char(string='11,小图标', default='')
    w_color = fields.Integer(string='12,颜色', default=10)

    w_partner_ids = fields.Many2many('res.partner', 'amos_demo_res_partner_rel', 'demo_id', 'partner_id',
                                     string='13,带用户头像')
    w_user_ids = fields.Many2many('res.users', 'amos_demo_res_users_rel', 'demo_id', 'partner_id',
                                  string='13,带用户头像')
    w_demo = fields.Char(string='15,过滤', default='')

    w_is_favorite = fields.Boolean(string='16,重点')

    w_document = fields.Binary('17,文件', attachment=False, )

    w_percentage = fields.Float('18,百分号', required=True, default=54, digits=(10, 2))

    w_color1 = fields.Integer(string='19,颜色', default=5)


    n_1 = fields.Char(string='不规则1', default='')
    n_2 = fields.Char(string='不规则2', default='')
    n_3 = fields.Char(string='不规则3', default='')
    n_4 = fields.Char(string='不规则4', default='')
    n_5 = fields.Char(string='不规则5', default='')

    n_6 = fields.Char(string='不规则6', default='')
    n_7 = fields.Char(string='不规则7', default='')
    n_8 = fields.Char(string='不规则8', default='')
    n_9 = fields.Char(string='不规则9', default='')


    @api.model
    def _select_objects(self):

        domain=[('model', '=', 'res.partner')]
        records = self.env['ir.model'].search(domain)
        return [(record.model, record.name) for record in records] + [('', '')]

    id_object = fields.Reference(string='20,关联标签', selection='_select_objects')

    def action_confirm(self):

        # t = xodoo.chinese_initials(values['name'])
        #
        # print(xodoo.version())
        #
        # print(t)

        return True

    def _cron_update_amos_demo(self):
        print('我来了')
        self.env['ir.config_parameter'].set_param('hd', '0000')

    @api.model
    def get_import_templates(self):
        res = super(amos_demo, self).get_import_templates()
        if self.env.context.get('purchase_product_template'):
            return [{
                'label': _('Import Template for Products'),
                'template': '/demo/static/xls/product_purchase.xls'
            }]
        return res

    def create_workflow(self):
        url = '/workflow?model=amos.demo&ttype=create'

        return {
            'type': 'ir.actions.act_url',
            'url': url,
        }

    def button_attachment(self):
        """
        上传附件与图片
        :return:
        """

        url = '/web/login'
        open = {}
        open['type'] = 2  # 可缺省 默认值为2  基本层类型：0（信息框，默认）1（页面层）2（iframe层，也就是解析content）3（加载层）4（tips层）
        open['title'] = "登陆"  # 可缺省 默认值为 空 窗口标题
        open['area'] = ['1000px', '680px']  # 窗口大小
        open['btn'] = ['确认']  # 可缺省 按钮：按钮1的回调是yes（也可以是btn1），而从按钮2开始，则回调为btn2: function(){}，以此类推

        return {
            'name': '登陆',
            'type': "ir.actions.act_url",
            'url': url,
            'target': 'open_iframe',
            'open': open,
        }

        context = dict(self._context or {})

        client_action = {'type': 'ir.actions.act_url',
                         'name': "可视化部局设计器",
                         'target': 'new',
                         'url': '/layout/%s/%s' % (context.get('type'), self.id),
                         }
        return client_action

    def button_rust_upload(self):
        #::::判断并生成相关的xodoo_token
        from dateutil.relativedelta import relativedelta
        import random
        # params = eval(self.env['ir.config_parameter'].sudo().get_param('go_upload', 'False'))
        local_upload_go = "http://%s/saas/ir_attachment/index" % odoo.tools.config.get('local_upload_rust','127.0.0.1:8010')

        context = dict(self._context or {})

        xodoo_token = self.env['xodoo.token'].sudo().search(
            [('user_id', '=', context.get('uid')), ('name', '=', 'Rust_Upload')], order="id desc", limit=1)
        if not xodoo_token:

            def _create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
                nowTime = datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
                randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
                if randomNum <= 10:
                    randomNum = str(0) + str(randomNum)
                uniqueNum = str(nowTime) + str(randomNum)
                return uniqueNum

            appid = _create_uuid()
            secret = uuid.uuid4().hex

            access_token = self.token(self.env.user.login, appid, secret)
            values = {
                "name": 'Rust_Upload',
                'user_id': context.get('uid'),
                'appid': appid,
                'secret': secret,
                'access_token': access_token,
                'token_date': fields.Datetime.now() + relativedelta(hours=+2),
                'date_start': fields.Date.today(),
                'date_end': fields.Date.today() + relativedelta(years=3),
            }
            self.env['xodoo.token'].sudo().create(values)
        else:
            if xodoo_token.token_date < fields.Datetime.now():
                access_token = self.token(self.env.user.login, xodoo_token.appid, xodoo_token.secret)
                values = {
                    'access_token': access_token,
                    'token_date': fields.Datetime.now() + relativedelta(hours=+10),
                }
                xodoo_token.sudo().write(values)
            else:
                access_token = xodoo_token.access_token


        res_model = context.get('res_model', self._name)
        mimetype = context.get('mimetype', '*')
        res_id = context.get('res_id', self.id)
        res_field = context.get('res_field', '')
        company_id = context.get('company_id', 1)
        create_uid = context.get('uid')
        write_uid = context.get('uid')
        title = context.get('title','文件上传')
        view_mode = context.get('view_mode','form')
        type = context.get('type','intg')
        import urllib.parse
        name = urllib.parse.quote('file')
        print(context)
        params_dict = {
            'res_model': res_model,
            'res_id': res_id,
            'res_field': res_field,
            'company_id': company_id,
            'create_uid': create_uid,
            'write_uid': write_uid,
            'mimetype': mimetype,
            'view_mode': view_mode,
            'access_token': access_token,
            'db_name': self.pool.db_name,
            'name': urllib.parse.quote('file'),
            'title': title,
            'offset': 0,
            'limit': 10,
        }

        if res_model == 'documents.document':
            params_dict['res_id'] = context.get('res_id', '')
            params_dict['folder_id'] = context.get('folder_id', 1)
            params_dict['preview'] = 1

        url = f"{local_upload_go}?{urllib.parse.urlencode(params_dict)}"

        return {
            'type': 'ir.actions.act_url',
            'url': url,
        }

    def button_rust_image(self):
        #::::判断并生成相关的xodoo_token
        from dateutil.relativedelta import relativedelta
        import random
        # params = eval(self.env['ir.config_parameter'].sudo().get_param('go_upload', 'False'))
        local_upload_go = "http://%s/index" % odoo.tools.config.get('local_upload_rust','127.0.0.1:9097')

        context = dict(self._context or {})

        xodoo_token = self.env['xodoo.token'].sudo().search(
            [('user_id', '=', context.get('uid')), ('name', '=', 'Rust_Upload')], order="id desc", limit=1)
        if not xodoo_token:

            def _create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
                nowTime = datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
                randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
                if randomNum <= 10:
                    randomNum = str(0) + str(randomNum);
                uniqueNum = str(nowTime) + str(randomNum);
                return uniqueNum

            appid = _create_uuid()
            secret = uuid.uuid4().hex

            access_token = self.token(self.env.user.login, appid, secret)
            values = {
                "name": 'Rust_Upload',
                'user_id': context.get('uid'),
                'appid': appid,
                'secret': secret,
                'access_token': access_token,
                'token_date': fields.Datetime.now() + relativedelta(hours=+2),
                'date_start': fields.Date.today(),
                'date_end': fields.Date.today() + relativedelta(years=3),
            }
            self.env['xodoo.token'].sudo().create(values)
        else:
            if xodoo_token.token_date < fields.Datetime.now():
                access_token = self.token(self.env.user.login, xodoo_token.appid, xodoo_token.secret)
                values = {
                    'access_token': access_token,
                    'token_date': fields.Datetime.now() + relativedelta(hours=+10),
                }
                xodoo_token.sudo().write(values)
            else:
                access_token = xodoo_token.access_token


        res_model = context.get('res_model', self._name)
        res_id = context.get('res_id', self.id)
        res_field = context.get('res_field', '')
        company_id = context.get('company_id', 1)
        create_uid = context.get('uid')
        write_uid = context.get('uid')
        import urllib.parse

        name = urllib.parse.quote('file')
        # url = '%s?res_model=%s&res_id=%s&res_field=%s&company_id=%s&create_uid=%s&write_uid=%s&access_token=%s&name=%s&mimetype=.doc,.zip,.png&offset=10' % (params.get('url'),res_model,res_id,res_field,company_id,create_uid,write_uid,access_token,'上传文件')

        # url = '%s?res_model=%s&res_id=%s&res_field=%s&company_id=%s&create_uid=%s&write_uid=%s&access_token=%s&name=%s&offset=10' % (params.get('url'),res_model,res_id,res_field,company_id,create_uid,write_uid,access_token,'上传文件')
        print(context)
        folder_id = context.get('folder_id', 1)
        if res_model == 'documents.document':
            res_id = context.get('res_id', '')
            url = '%s?res_model=%s&res_id=%s&res_field=%s&company_id=%s&create_uid=%s&write_uid=%s&access_token=%s&name=%s&offset=10&folder_id=%s&preview=1' % (
            local_upload_go, res_model, res_id, res_field, company_id, create_uid, write_uid, access_token, name,
            folder_id)
        else:
            url = '%s?res_model=%s&res_id=%s&res_field=%s&company_id=%s&create_uid=%s&write_uid=%s&access_token=%s&name=%s&offset=10' % (
                local_upload_go, res_model, res_id, res_field, company_id, create_uid, write_uid, access_token, name)



        return {
            'type': 'ir.actions.act_url',
            'url': url,
        }


    def token(self, login, appid, secret):
        """
        token加密
        :param login:
        :param appid:
        :param secret:
        :return:
        """
        import hashlib
        API_SECRET = "xodoo"  # 从接口对接负责人处拿到
        # login = "xxxx"  # GET传递的项目编码，用户登陆帐号
        # appid = "xxxx"  # GET传递的登录帐号，凭证
        # time_stamp = str(t_stamp())  # int型的时间戳必须转化为str型，否则运行时会报错
        today = fields.Date.today()
        hl = hashlib.md5()  # 创建md5对象，由于MD5模块在python3中被移除，在python3中使用hashlib模块进行md5操作
        strs = login + appid + secret + str(today) + API_SECRET  # 根据token加密规则，生成待加密信息
        hl.update(
            strs.encode("utf8"))  # 此处必须声明encode， 若为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
        token = hl.hexdigest()  # 获取十六进制数据字符串值
        # print('MD5加密前为 ：', strs)
        # print('MD5加密后为 ：', token)
        return token




class amos_demo_line(models.Model):
    _name = "amos.demo.line"
    _description = "演示工作流明细"
    _order = 'sequence asc'

    sequence = fields.Integer(string='排序', default=10)

    name = fields.Char(string='项目名称')
    order_id1 = fields.Many2one('amos.demo', string=u'明细', required=True, ondelete='cascade', index=True, copy=False)

    state = fields.Selection([
        ('新建', '新建'),
        ('校对', '校对'),
        ('审核', '审核'),
        ('批准', '批准'),
        ('已发布', '已发布'),
    ], string='状态', default='新建')

    @api.model
    def create(self, vals):
        context = dict(self._context or {})
        print(context)
        line = super(amos_demo_line, self).create(vals)
        return line
