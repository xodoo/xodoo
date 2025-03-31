# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# XMLPRC全功能演示 Demo
# QQ:35350428
# 邮件:sale@100china.cn
# 手机：13584935775
# 作者：'wangguangjian'
# 公司网址： www.odoo.pw  www.100china.cn
# Copyright 昆山一百计算机有限公司 2012-2017 Amos
# 日期：2017-11-18
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import xmlrpc.client as xodoo

url = 'http://127.0.0.1:9099'
db = 'xodoo'
username = 'admin'
password = '1'

#:::::::::::::::2::::::::当前系统版本
common = xodoo.ServerProxy('{}/xmlrpc/2/common'.format(url))
# version = common.version()
# print(version)

#:::::::::::::::3::::::::当前用户的数字ID
uid = common.authenticate(db, username, password, {})
# print(uid)

#:::::::::::::::4::::::::调用方法
# 每次调用execute_kw需要下列参数：
# 要使用的数据库，db
# 用户ID（通过身份验证检索），uid
# 用户的密码、username,password
# 模型名、如：res.partner
# 方法名、read
# 通过位置传递的数组/参数列表
#
models = xodoo.ServerProxy('{}/xmlrpc/2/object'.format(url))
is_rights = models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights',
                              ['read'], {'raise_exception': False})

# print(is_rights)
#
# #:::::::::::::::5::::::::查询
ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
# print(ids)#
#
# #:::::::::::::::6::::::::查询返回指定行数  从第十条开始 向后取5个值
ids= models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'offset': 1, 'limit': 5})

# print(ids)#
#
#
# #:::::::::::::::7::::::::查询返记录总数
#
count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])

# print(count)
#
# #:::::::::::::::8::::::::查询符合条件的ID 再用id查询对象全部记录信息

ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'limit': 1})
[record] = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids])

# print(len(record))
#
#
# #:::::::::::::::9::::::::查询指定记录的字段信息
#
value = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids], {'fields': ['name', 'country_id', 'comment']})

# print(value)
#
#
#
# #:::::::::::::::10::::::::可以返回字段的属性信息
attributes =models.execute_kw(db, uid, password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
# print(attributes)
#
# #:::::::::::::::11::::::::查询并读取5条信息
#
value =models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

# print(value)
#
# #:::::::::::::::12::::::::创建一条记录并返回数据id
partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': "New Partner"}])

# print(partner_id)
#
# #:::::::::::::::13::::::::对上一条创建记录进行修改
obj = models.execute_kw(db, uid, password, 'res.partner', 'write', [[partner_id], {'name': "Newer partner1111"}])
# print(obj)
partner = models.execute_kw(db, uid, password, 'res.partner', 'read', [[partner_id], ['display_name']])
# print(partner)

#
#
# #:::::::::::::::14::::::::对上一条创建记录进行删除操作

obj = models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partner_id]])
# print(obj)
list = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['id', '=', partner_id]]])
# print(list)

#
# #:::::::::::::::18::::::::报表输出
# #
# #
# # invoice_ids = models.execute_kw(
# #     db, uid, password, 'amos.class', 'search',
# #     [[('type', '=', 'out_invoice'), ('state', '=', 'open')]])
# report = xodoo.ServerProxy('{}/xmlrpc/2/report'.format(url))
# result = report.render_report(db, uid, password, 'amosclass.amos_class_full', [16])
# report_data = result['result'].decode('base64')
#
# print report_data
#
#
#
#