# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# odoo Connector
# QQ:35350428
# 邮件:35350428@qq.com
# 手机：13584935775
# 作者：'Amos'
# 公司网址： www.odoo.pw  www.100china.cn  http://i.youku.com/amoserp
# Copyright 昆山一百计算机有限公司 2012-2018 Amos
# 日期：2018-3-19
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import datetime
from dateutil import parser
import re
import odoo
import base64
from urllib import parse
import yaml
import json
import random
from datetime import datetime, date, timezone, timedelta


def date_format(value, format=''):
    if value == '':
        return ''
    if format == '':
        format = '%Y-%m-%d %H:%M:%S'
        data = (value + timedelta(hours=8)).strftime(format)
        return parser.parse(data).date()
    else:
        if value:
            data = (value + timedelta(hours=8)).strftime(format)
        else:
            return ''
        return parser.parse(data)


def date_filter(value, a,z):
    if value==False:
        return value
    else:
        format = '%Y-%m-%d %H:%M:%S'
        data = (value + timedelta(hours=8)).strftime(format)
        return str(data)[a:z]



def reverse_filter(s):
    return s[0:1]


def max_list(s):
    """
    列表取最大值
    :param s:
    :return:
    """
    v = max(s)
    return v * 1.25

def decode(s):
    if s != False:
        return s.decode('utf-8')
    return s


def split(str,separate,number):
    """
    str:字符串
    separate:分割符
    number:取值
    """
    return str.split(separate)[number]

def list_split(str,separate):
    """
    str:字符串
    separate:分割符
    number:取值
    """
    return str.split(separate)

# def section_filter(s,n):
#     return str(s)[0:n]

def section_filter(s,a,z):
    return str(s)[a:z]


##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_Format_Html(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    re_stopwords=re.compile('\u3000')#去除无用的'\u3000'字符
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    s=re_stopwords.sub('',s)
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}

    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr



def analysis_values(kw):
    """
    字段参数格式化,后面优化解析方式
    支持全局使用
    :param kw:
    :return:
    """
    parm = {}
    for key in kw.keys():
        if key.find('form-field-boolean-') != -1:
            if kw[key] == 'False':
                parm[key.replace('form-field-boolean-', '')] = False
            else:
                parm[key.replace('form-field-boolean-', '')] = kw[key]
        elif key.find('form-field-char-') != -1:
            if kw[key] == 'False':
                parm[key.replace('form-field-char-', '')] = ''
            else:
                parm[key.replace('form-field-char-', '')] = kw[key]

        elif key.find('form-field-integer-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-integer-', '')] = 0
            else:
                parm[key.replace('form-field-integer-', '')] = int(kw[key])

        elif key.find('form-field-many2one-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-many2one-', '')] = False
            else:
                parm[key.replace('form-field-many2one-', '')] = int(kw[key])

        elif key.find('form-field-float-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-float-', '')] = 0
            else:
                parm[key.replace('form-field-float-', '')] = float(kw[key])

        elif key.find('form-field-date-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-date-', '')] = False
            else:
                d = datetime.strptime(kw[key], '%Y-%m-%d')
                parm[key.replace('form-field-date-', '').replace('.', '_')] = d

        elif key.find('form-field-datetime-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-datetime-', '')] = False
            else:
                d = datetime.strptime(kw[key], '%Y-%m-%d %H:%M:%S')
                parm[key.replace('form-field-datetime-', '').replace('.', '_')] = d

        elif key.find('form-field-html-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-html-', '')] = ''
            else:
                parm[key.replace('form-field-html-', '')] = kw[key]

        elif key.find('form-field-text-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-text-', '')] = ''
            else:
                parm[key.replace('form-field-text-', '')] = kw[key]
        elif key.find('form-field-radio-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-radio-', '')] = ''
            else:
                parm[key.replace('form-field-radio-', '')] = kw[key]

        elif key.find('form-field-select-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-select-', '').replace('.', '_')] = ''
            else:
                parm[key.replace('form-field-select-', '').replace('.', '_')] = kw[key]

        elif key.find('form-field-binary-') != -1:
            if kw[key] == 'False' or kw[key] == '':
                parm[key.replace('form-field-binary-', '')] = ''
            else:
                parm[key.replace('form-field-binary-', '')] = kw[key]

        # :::::::::::::::::::::::::::::::::::many2many 6 字段提交 开始
        # for key in kw.keys():
        if key.find('form-field-m2m') != -1:
            m2m_arr = []
            m2m_fields = ''
            many2many = 6
            # 对一个Many2Many 6 字进行处理
            if key.find('form-field-m2m0?') != -1:
                many2many = 0
                m2m_arr.append(kw[key])
                m2m_fields = key.split('?')[1].replace('.', '_')
            elif key.find('form-field-m2m6?') != -1:
                many2many = 6
                m2m_arr = kw[key]
                m2m_fields = key.split('?')[1].replace('.', '_')
            elif key.find('form-field-m2m5?') != -1:
                many2many = 5
                m2m_arr.append(kw[key])
                m2m_fields = key.split('?')[1].replace('.', '_')
            elif key.find('form-field-m2m4?') != -1:
                many2many = 4
                m2m_arr.append(kw[key])
                m2m_fields = key.split('?')[1].replace('.', '_')
            elif key.find('form-field-m2m3?') != -1:
                many2many = 3
                m2m_arr.append(kw[key])
                m2m_fields = key.split('?')[1].replace('.', '_')
            elif key.find('form-field-m2m2?') != -1:
                many2many = 2
                m2m_arr.append(kw[key])
                m2m_fields = key.split('?')[1].replace('.', '_')
            elif key.find('form-field-m2m1?') != -1:
                many2many = 1
                m2m_arr.append(kw[key])
                m2m_fields = key.split('?')[1].replace('.', '_')
            # ::::进行数据绑定
            if len(m2m_arr) > 0:
                # m2m_arr = map(int, m2m_arr)
                if many2many == 0:  # (0,0,{values}) 根据values里面的信息新建一个记录
                    parm[m2m_fields] = [(0, 0, 2)]
                elif many2many == 6:  # (6,0,[IDs]) 用IDs里面的记录替换原来的记录（就是先执行(5)再执行循环IDs执行（4,ID））
                    v = eval(m2m_arr)
                    if isinstance(v,int) == 1:
                        v = [int(m2m_arr)]
                    parm[m2m_fields] = [(6, 0, v)]
                elif many2many == 5:  # (5) 删除所有的从数据的链接关系就是向所有的从数据调用(3,ID)
                    parm[m2m_fields] = [(5)]
                elif many2many == 4:  # (4,ID) 为id=ID的数据添加主从链接关系。
                    parm[m2m_fields] = [(4, int(m2m_arr[0]))]
                elif many2many == 3:  # (3,ID) 切断主从数据的链接关系但是不删除这个数据
                    parm[m2m_fields] = [(3, int(m2m_arr[0]))]
                elif many2many == 2:  # (2,ID) 删除id=ID的数据（调用unlink方法，删除数据以及整个主从数据链接关系）
                    parm[m2m_fields] = [(2, m2m_arr)]
                elif many2many == 1:  # (1,ID,{values})更新id=ID的记录（写入values里面的数据）
                    parm[m2m_fields] = [(1, m2m_arr)]
        # :::::::::::::::::::::::::::::::::::many2many 字段提交 结束
    # print (parm)
    return parm

def past_time(time):
    """ 返回time距离现在的时间是多久 """
    print(type(time))
    print(time)
    print(datetime.now())
    timestamp = (datetime.now() - time).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif timestamp >= 60 and timestamp < 60 * 60:
        return f'{int(timestamp / 60)} 分钟前'
    elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
        return f'{int(timestamp / (60 * 60))} 小时前'
    elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
        return f'{int(timestamp / (60 * 60 * 24))} 天前'
    else:
        return time.strftime('%Y-%m-%d %H:%M')


def _get_models_attachment_list(self,order,kw,limit):
    """
    标准的单据附件
    :param self:
    :param order:
    :param kw:
    :return:
    """
    attachment_ids = []
    domain = [('res_model', '=', order._name), ('res_id', '=', order.id)]
    attachment = self.env['ir.attachment'].sudo().search(domain, order="id desc", limit=limit)
    for k in attachment:
        attachment = _get_files_type(k, kw.get('http_host'))
        http_host = kw.get('http_host').split(':')
        preview_url = ''
        if k.file_path:
            if odoo.tools.config.get('preview_url'):
                http = odoo.tools.config.get('preview_url')
                file = '%s%s' % (http, k.file_path.replace('./gofiles', ''))
                result = base64.b64encode(file.encode()).decode('utf8')
                preview_url = '%s/onlinePreview?url=%s' % (http, parse.quote(result))
            else:
                file = '%s%s:8021%s' % (http_host[0],http_host[1],k.file_path.replace('./gofiles',''))
                result = base64.b64encode(file.encode()).decode('utf8')
                preview_url = '%s%s:8021/onlinePreview?url=%s' % (http_host[0], http_host[1], parse.quote(result))
        else:
            download_file = '/ad/content/%s-%s?download=true' % (str(k.id), k.checksum)
            if odoo.tools.config.get('preview_url'):
                http = odoo.tools.config.get('preview_url')
                file = '%s%s' % (http, download_file)
                result = base64.b64encode(file.encode()).decode('utf8')
                preview_url = '%s/onlinePreview?url=%s' % (http, parse.quote(result))
            else:
                file = '%s%s:8021%s' % (http_host[0], http_host[1], download_file)
                result = base64.b64encode(file.encode()).decode('utf8')
                preview_url = '%s%s:8021/onlinePreview?url=%s' % (http_host[0], http_host[1], parse.quote(result))

        t = {
            'id': attachment.get('id'),
            'icon': attachment.get('icon'),
            "create_date": attachment.get('create_date'),
            "write_date": attachment.get('write_date'),
            "past_time": past_time(order.write_date),  # 过去时间
            'name': attachment.get('name'),
            'url': attachment.get('url'),
            'preview_url': preview_url,
        }
        attachment_ids.append(t)
    return attachment_ids


def _get_files_type(attachment, http_host):
    """
    软件格式转换
    :param attachment:
    :param http_host:
    :return:
    """
    if attachment.type == 'url':
        url = attachment.url
    else:
        url = '%s/ad/image/%s-%s' % (http_host, attachment.id, attachment.checksum)

    value = {
        'icon': '%s/Amos_CRM/static/src/img/ico_file_mini.svg' % http_host,
        'type': 'other',
        'id': attachment.id,
        'checksum': attachment.checksum,
        'file_size': attachment.file_size,  # 文件大小
        'name': attachment.name,
        'url': url,
        "create_date": date_filter(attachment.create_date, 0, 19),  # 创建日期
        "write_date": date_filter(attachment.write_date, 0, 19),  # 最近修改日期
        "past_time": past_time(attachment.create_date),  # 过去时间
    }

    #图片
    if attachment.mimetype in ['image/png', 'image/jpg', 'image/gif', 'image/bmp', 'image/jpeg']:
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_pic_mini.svg' % http_host
        value['type'] = 'image'
        return value

    #::::下载地址一致
    if attachment.type == 'url':
        url = attachment.url
    else:
        url = '%s/ad/content/%s-%s' % (http_host, attachment.id, attachment.checksum)

    value['url'] = url
    #视频
    if attachment.mimetype in ['video/mp4']:
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_video_mini.svg' % http_host
        value['type'] = 'video'
        return value
    #音频
    if attachment.mimetype in ['audio/mpeg', 'video/aac', 'application/octet-stream']:
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_audio_mini.svg' % http_host
        value['type'] = 'audio'
        return value
    #PDF
    if attachment.mimetype == 'application/pdf':
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_pdf_mini.svg' % http_host
        value['type'] = 'pdf'
        return value
    #PPT
    if attachment.mimetype ==  'application/vnd.openxmlformats-officedocument.presentationml.presentation':
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_pptx_mini.svg' % http_host
        value['type'] = 'ppt'
        return value
    #XLS
    if attachment.mimetype ==  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_xlsx_mini.svg' % http_host
        value['type'] = 'xls'
        return value
    #ZIP
    if attachment.mimetype ==  'application/zip':
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_zip_mini.svg' % http_host
        value['type'] = 'zip'
        return value
    #DOC
    if attachment.mimetype in ['application/msword',
                                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_doc_mini.svg' % http_host
        value['type'] = 'doc'
        return value
    #CSV
    if attachment.mimetype == 'text/csv':
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_csv_mini.svg' % http_host
        value['type'] = 'csv'
        return value
    # 超链
    if attachment.mimetype == 'application' and attachment.type == 'url':
        value['icon'] = '%s/Amos_CRM/static/src/img/ico_link_mini.svg' % http_host
        value['type'] = 'link'
        return value
    return value


def odooapijsonres(data, status=200, code=1, msg="成功", sysMsg="success"):
    '''
    :param data:返回的数据
    :param status: 状态
        200: OK
        400: Bad Request
        500：Internal Server Error
        401：Unauthorized
        403：Forbidden
        404：Not Found
    :param code: 编码  1: 获取数据成功 | 操作成功     0：获取数据失败 | 操作失败
    :param msg:
    :param sysMsg:
    :return:
    '''
    res = {
        "status": status,
        "code": code,
        "data": data,
        "msg": msg,
        "sysMsg": sysMsg
    }
    return res

def generate_code(len=6):
    dtstr = ""
    for i in range(len):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        dtstr += ch
    return dtstr


def generate_code_alphanum(length=10):
    code = ''
    for i in range(length):
        big_letter = chr(random.randint(65, 90))  # 大写字母
        small_letter = chr(random.randint(97, 122))  # 小写字母
        num = str(random.randint(0, 9))
        code += random.choice([big_letter, small_letter, num])
    return code


# 重写json类
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def get_now():
    now = datetime.now(timezone(timedelta(hours=8)))
    return now

def get_nownoon():
    nownoon = datetime.strptime(str(datetime.now(timezone(timedelta(hours=8))).date()) + " 12:00:00", "%Y-%m-%d %H:%M:%S")
    return nownoon

def get_now00():
    now00 = datetime.combine(datetime.now(timezone(timedelta(hours=8))).date(), datetime.min.time())
    return now00

def get_now24():
    now24 = datetime.combine(datetime.now(timezone(timedelta(hours=8))).date(), datetime.max.time())
    return now24

def get_nowdate():
    now = datetime.now(timezone(timedelta(hours=8))).date()
    return now

def test_generate_code():
    leng=6
    res = generate_code(leng)
    print("res:{}".format(res))



def read(path):
    with open(path, 'r') as file:
        data = file.read()
        # result = yaml.Loader(data)
        result = yaml.load(data, Loader=yaml.FullLoader)
        return result
