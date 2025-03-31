# encoding:utf-8
# ----------------------------------------------------------
# 代码测试成功后 转 apipost
# 接口地址为：https://docs.apipost.cn/preview/11ade58a33f4a394/fa132ae8a13d7d25?target_id=8d645e54-f7c8-4437-b425-4464ad7416b5#8d645e54-f7c8-4437-b425-4464ad7416b5
# ----------------------------------------------------------
import requests
import datetime

#::::::测试网址
# url = 'http://122.51.164.176:8072'  #正式服务器测试端口
url = 'http://106.14.155.204:8069'  # 本地测试端口
url = 'http://127.0.0.1:9099/'  # 本地测试端口

#:::::: 0 标准用户登陆-用帐号与密码登陆
data = {
    'login': 'admin',
    'password': '1',
    'type': '0',  # 0：用帐号与密码登陆  1：手机验证码登陆  2，发送手机验证码，3：微信扫码登陆  4，APP验证码登陆
}
r = requests.post('%s/api/v1/login/0' % url, data=data)
print(r.text.encode('utf-8').decode('unicode_escape'))
v = eval(r.text)




#部门
postdata = {
    'access_token': v['data']['access_token'],  #获取access_token 每天不一样目前
    'model': 'hr.department',         #当前对象
    'uid': v['data']['uid'],                    #当前用户 uid
    'partner_id': v['data']['partner_id'],      #当前用户partner_id
    'function_name': '_api_xodoo_page',               #用户接口名称

    'domain': "[('parent_id', '=', False)]",
    'search': '',                               #查询关键字
    'page': 0,                                  #从第几页开始
    'limit': 10,                                #每页显示数量
    'order': 'id desc',                         #排序
}
r = requests.post('%s/api/v1/getattr/0' % url, data=postdata)
print(r.text.encode('utf-8').decode('unicode_escape'))