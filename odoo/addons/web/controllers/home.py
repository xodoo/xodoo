# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import psycopg2

import odoo.exceptions
import odoo.modules.registry
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.service import security
from odoo.tools.translate import _
from .utils import (
    ensure_db,
    _get_login_redirect_url,
    is_user_internal,
)
# TODO(amos): add
from odoo.release import product_name
from .utils import ensure_db, _get_login_redirect_url, is_user_internal

_logger = logging.getLogger(__name__)

# Shared parameters for all login/signup flows
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'signup_email'}
LOGIN_SUCCESSFUL_PARAMS = set()
CREDENTIAL_PARAMS = ['login', 'password', 'type']

#:::访问static静态文件
# TODO(amos): amos add
import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/src/templates")
env = Environment(loader=templateLoader)
# TODO(amos): add
from odoo import release


class Home(http.Controller):

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        if request.db and request.session.uid and not is_user_internal(request.session.uid):
            return request.redirect_query('/web/login_successful', query=request.params)
        return request.redirect_query('/odoo', query=request.params)

    def _web_client_readonly(self):
        return False

    # ideally, this route should be `auth="user"` but that don't work in non-monodb mode.
    @http.route(['/web', '/odoo', '/odoo/<path:subpath>', '/scoped_app/<path:subpath>'], type='http', auth="none",
                readonly=_web_client_readonly)
    def web_client(self, s_action=None, **kw):

        # Ensure we have both a database and a user
        ensure_db()
        if not request.session.uid:
            return request.redirect_query('/web/login', query={'redirect': request.httprequest.full_path}, code=303)
        if kw.get('redirect'):
            return request.redirect(kw.get('redirect'), 303)
        if not security.check_session(request.session, request.env, request):
            raise http.SessionExpiredException("Session expired")
        if not is_user_internal(request.session.uid):
            return request.redirect('/web/login_successful', 303)

        # Side-effect, refresh the session lifetime
        request.session.touch()

        # Restore the user on the environment, it was lost due to auth="none"
        request.update_env(user=request.session.uid)
        try:
            if request.env.user:
                request.env.user._on_webclient_bootstrap()
            context = request.env['ir.http'].webclient_rendering_context()
            response = request.render('web.webclient_bootstrap', qcontext=context)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        except AccessError:
            return request.redirect('/web/login?error=access')

    @http.route('/web/webclient/load_menus/<string:unique>', type='http', auth='user', methods=['GET'], readonly=True)
    def web_load_menus(self, unique, lang=None):
        """
        Loads the menus for the webclient
        :param unique: this parameters is not used, but mandatory: it is used by the HTTP stack to make a unique request
        :param lang: language in which the menus should be loaded (only works if language is installed)
        :return: the menus (including the images in Base64)
        """
        if lang:
            request.update_context(lang=lang)

        menus = request.env["ir.ui.menu"].load_web_menus(request.session.debug)
        body = json.dumps(menus)
        response = request.make_response(body, [
            # this method must specify a content-type application/json instead of using the default text/html set because
            # the type of the route is set to HTTP, but the rpc is made with a get and expects JSON
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'public, max-age=' + str(http.STATIC_CACHE_LONG)),
        ])
        return response

    # TODO(Amos): add
    @http.route('/web/assets/load_menus/<string:unique>', type='http', auth='user', methods=['GET'])
    def web_assets_load_menus(self, unique, lang=None):

        print(request.session.debug)
        debug_url = request.session.debug
        if debug_url != "":
            debug_url = "?debug=%s" % debug_url

        menus = request.env['ir.ui.menu'].load_web_menus(request.session.debug)

        if unique == '1234':
            menus = self._get_menus(menus,debug_url)
            return menus

        if lang:
            request.update_context(lang=lang)

        menus = request.env["ir.ui.menu"].load_web_menus(request.session.debug)
        body = json.dumps(menus, indent=4, ensure_ascii=False)
        response = request.make_response(body, [
            # this method must specify a content-type application/json instead of using the default text/html set because
            # the type of the route is set to HTTP, but the rpc is made with a get and expects JSON
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'public, max-age=' + str(http.STATIC_CACHE_LONG)),
        ])
        return response

    # TODO(Amos): add
    def _get_menus(self, menus,debug_url):
        """
        自定义用户菜单
        增缓存变量
        SQL查询，权限绑定
        """

        menus = {61: {'id': 61, 'name': '用户', 'font_icon': '', 'children': [], 'appID': 1, 'xmlid': 'base.menu_action_res_users', 'actionID': 70, 'actionModel': 'ir.actions.act_window', 'actionPath': 'users'}, 67: {'id': 67, 'name': '一般设置', 'font_icon': '', 'children': [], 'appID': 1, 'xmlid': 'base_setup.menu_config', 'actionID': 85, 'actionModel': 'ir.actions.act_window', 'actionPath': 'settings'}, 107: {'id': 107, 'name': '任务中心', 'font_icon': '', 'children': [], 'appID': 107, 'xmlid': 'xodoo.menu_mail_activity', 'actionID': 150, 'actionModel': 'ir.actions.act_window', 'actionPath': False}, 108: {'id': 108, 'name': '测试1', 'font_icon': '', 'children': [], 'appID': 108, 'xmlid': 'xodoo.menu_xodoo_res_partner', 'actionID': 151, 'actionModel': 'ir.actions.act_window', 'actionPath': False}, 3: {'id': 3, 'name': '用户和公司', 'font_icon': '', 'children': [61, 58], 'appID': 1, 'xmlid': 'base.menu_users', 'actionID': False, 'actionModel': False, 'actionPath': False}, 70: {'id': 70, 'name': '配置', 'font_icon': '', 'children': [71, 72, 73], 'appID': 69, 'xmlid': 'mail.menu_configuration', 'actionID': False, 'actionModel': False, 'actionPath': False}, 71: {'id': 71, 'name': '通知', 'font_icon': '', 'children': [], 'appID': 69, 'xmlid': 'mail.menu_notification_settings', 'actionID': 124, 'actionModel': 'ir.actions.client', 'actionPath': False}, 48: {'id': 48, 'name': '应用', 'font_icon': 'mdi mdi-view-grid-outline', 'children': [49, 52, 51], 'appID': 15, 'xmlid': 'base.menu_apps', 'actionID': False, 'actionModel': False, 'actionPath': False}, 49: {'id': 49, 'name': '主要应用', 'font_icon': 'mdi mdi-order-bool-ascending-variant', 'children': [], 'appID': 15, 'xmlid': 'base.menu_module_tree', 'actionID': 39, 'actionModel': 'ir.actions.act_window', 'actionPath': 'apps'}, 69: {'id': 69, 'name': '讨论', 'font_icon': '', 'children': [70], 'appID': 69, 'xmlid': 'mail.menu_root_discuss', 'actionID': 108, 'actionModel': 'ir.actions.client', 'actionPath': 'discuss'}, 72: {'id': 72, 'name': '语音和视频', 'font_icon': '', 'children': [], 'appID': 69, 'xmlid': 'mail.menu_call_settings', 'actionID': 125, 'actionModel': 'ir.actions.client', 'actionPath': False}, 52: {'id': 52, 'name': '主题商店', 'font_icon': 'mdi mdi-cart', 'children': [], 'appID': 15, 'xmlid': 'base.menu_theme_store', 'actionID': 41, 'actionModel': 'ir.actions.act_url', 'actionPath': False}, 58: {'id': 58, 'name': '公司', 'font_icon': '', 'children': [], 'appID': 1, 'xmlid': 'base.menu_action_res_company_form', 'actionID': 53, 'actionModel': 'ir.actions.act_window', 'actionPath': 'companies'}, 73: {'id': 73, 'name': '预设回复', 'font_icon': '', 'children': [], 'appID': 69, 'xmlid': 'mail.menu_canned_responses', 'actionID': 109, 'actionModel': 'ir.actions.act_window', 'actionPath': False}, 51: {'id': 51, 'name': '第三方应用程序', 'font_icon': 'mdi mdi-apps-box', 'children': [], 'appID': 15, 'xmlid': 'base.menu_third_party', 'actionID': 40, 'actionModel': 'ir.actions.act_url', 'actionPath': False}, 106: {'id': 106, 'name': '默认值', 'font_icon': '', 'children': [], 'appID': 106, 'xmlid': 'xodoo.menu_default_wizard', 'actionID': 149, 'actionModel': 'ir.actions.act_window', 'actionPath': False}, 15: {'id': 15, 'name': '应用', 'font_icon': 'mdi mdi-apps', 'children': [48], 'appID': 15, 'xmlid': 'base.menu_management', 'actionID': 39, 'actionModel': 'ir.actions.act_window', 'actionPath': 'apps'}, 1: {'id': 1, 'name': '设置', 'font_icon': 'mdi mdi-cog-outline', 'children': [67, 3], 'appID': 1, 'xmlid': 'base.menu_administration', 'actionID': 85, 'actionModel': 'ir.actions.act_window', 'actionPath': 'settings'}, 'root': {'id': 'root', 'name': 'root', 'children': [107, 108, 69, 106, 15, 1], 'appID': False, 'xmlid': '', 'actionID': False, 'actionModel': False, 'actionPath': False}}

        limenus = ''
        #:::查询所有菜单
        root = menus.get('root')


        # 一级模板:只有一个节点
        menu1 = """<li>
                          <a href="/odoo/%s">
                              %s
                              <span>%s</span>
                          </a>
                     </li>"""
        # 如果有下一个执行新的模板
        menu1_children = """<li><a href="%s"  class="has-arrow">
                                      %s
                                      <span>%s</span>
                                  </a> <ul class="sub-menu" aria-expanded="false">%s</ul></li>"""

        for line in root.get('children'):
            # 判断一级是否有下级

            node1 = menus.get(line).get('children')

            if node1:
                node_html = ''
                node_html += self._get_node1(node1, menus,debug_url)

                font_icon = ''
                if menus.get(line).get('font_icon'):
                    font_icon = '<i class="%s"></i>' % menus.get(line).get('font_icon')

                url = menus.get(line).get('actionPath', '')
                if url:
                    url = 'action-%s%s' % (menus.get(line).get('actionID', ''),debug_url)
                    if url == 'action-False':
                        url = 'javascript: void(0);'
                else:
                    url = 'javascript: void(0);'

                limenus += menu1_children % (url, font_icon, menus.get(line).get('name'), node_html)

            else:
                font_icon = ''
                if menus.get(line).get('font_icon'):
                    font_icon = '<i class="%s"></i>' % menus.get(line).get('font_icon')

                url = menus.get(line).get('actionPath', '')
                if url != 'False':
                    url = 'action-%s%s' % (menus.get(line).get('actionID', ''),debug_url)
                else:
                    url = 'action-%s%s' % (menus.get(line).get('actionID', ''),debug_url)
                # limenus += menu1 % (menus.get(url, font_icon, menus.get(line).get('name'))
                limenus += menu1 % (url, font_icon, menus.get(line).get('name'))

        data = {
            "menus": limenus,
        }
        return json.dumps(data)

    # TODO(Amos): add
    def _get_node1(self, node1, menus,debug_url):
        """
        用户第一个节点
        """
        limenus = ''
        # 一级模板:只有一个节点
        menu1 = """<li>
                          <a href="/odoo/%s">
                             %s
                              <span>%s</span>
                          </a>
                     </li>"""
        # 如果有下一个执行新的模板
        menu1_children = """<li><a href="%s"  class="has-arrow">
                                      %s
                                       <span>%s</span>
                                  </a> <ul class="sub-menu" aria-expanded="false">%s</ul></li>"""
        for line in node1:
            node1 = menus.get(line).get('children')
            if node1:
                node_html = ''
                node_html += self._get_node1(node1, menus,debug_url)

                font_icon = ''
                if menus.get(line).get('font_icon'):
                    font_icon = '<i class="%s"></i>' % menus.get(line).get('font_icon')

                url = menus.get(line).get('actionPath')
                if url == False:
                    url = 'action-%s' % menus.get(line).get('actionID')
                    if url == 'action-False':
                        url = 'javascript: void(0);'
                    else:
                        url = 'action-%s%s' % (menus.get(line).get('actionID'), debug_url)

                else:
                    url = 'javascript: void(0);'

                limenus += menu1_children % (url, font_icon, menus.get(line).get('name'), node_html)
            else:
                font_icon = ''
                if menus.get(line).get('font_icon'):
                    font_icon = '<i class="%s"></i>' % menus.get(line).get('font_icon')

                url = menus.get(line).get('actionPath')
                if url == False:
                    url = 'action-%s%s' % (menus.get(line).get('actionID'),debug_url)
                limenus += menu1 % (url, font_icon, menus.get(line).get('name'))

        return limenus

    def _login_redirect(self, uid, redirect=None):
        return _get_login_redirect_url(uid, redirect)

    @http.route('/web/login', type='http', auth='none', readonly=False)
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        # simulate hybrid auth=user/auth=public, despite using auth=none to be able
        # to redirect users when no db is selected - cfr ensure_db()
        if request.env.uid is None:
            if request.session.uid is None:
                # no user -> auth=public with specific website public user
                request.env["ir.http"]._auth_method_public()
            else:
                # auth=user
                request.update_env(user=request.session.uid)

        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            try:
                credential = {key: value for key, value in request.params.items() if key in CREDENTIAL_PARAMS and value}
                credential.setdefault('type', 'password')
                auth_info = request.session.authenticate(request.db, credential)
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(auth_info['uid'], redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        #::::查询一下
        # TODO(amos): amos write
        auth = request.env['ir.module.module'].sudo().search([('name', '=', 'auth_oauth')], limit=1)
        values['auth_oauth'] = False
        if auth:
            if auth.state == 'installed':
                values['auth_oauth'] = True

        values['company'] = request.env['res.company'].sudo().browse(1)
        values['release'] = release

        values['csrf_token'] = request.csrf_token()
        values['session_db'] = request.session.db

        template = env.get_template('login/zh_CN/login.html')
        html = template.render(object=values)
        return html

        # response = request.render('web.login', values)
        # response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        # response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        # return response

    @http.route('/web/login_successful', type='http', auth='user', website=True, sitemap=False)
    def login_successful_external_user(self, **kwargs):
        """Landing page after successful login for external users (unused when portal is installed)."""
        valid_values = {k: v for k, v in kwargs.items() if k in LOGIN_SUCCESSFUL_PARAMS}
        return request.render('web.login_successful', valid_values)

    @http.route('/web/become', type='http', auth='user', sitemap=False, readonly=True)
    def switch_to_admin(self):
        uid = request.env.user.id
        if request.env.user._is_system():
            uid = request.session.uid = odoo.SUPERUSER_ID
            # invalidate session token cache as we've changed the uid
            request.env.registry.clear_cache()
            request.session.session_token = security.compute_session_token(request.session, request.env)

        return request.redirect(self._login_redirect(uid))

    @http.route('/web/health', type='http', auth='none', save_session=False)
    def health(self, db_server_status=False):
        health_info = {'status': 'pass'}
        status = 200
        if db_server_status:
            try:
                odoo.sql_db.db_connect('postgres').cursor().close()
                health_info['db_server_status'] = True
            except psycopg2.Error:
                health_info['db_server_status'] = False
                health_info['status'] = 'fail'
                status = 500
        data = json.dumps(health_info)
        headers = [('Content-Type', 'application/json'),
                   ('Cache-Control', 'no-store')]
        return request.make_response(data, headers, status=status)

    @http.route(['/robots.txt'], type='http', auth="none")
    def robots(self, **kwargs):
        return "User-agent: *\nDisallow: /\n"
