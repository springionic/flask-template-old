# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16

import json

from flask import g, Flask
from flask import request

from routes import blueprint_list


def register_middleware(app: Flask) -> ...:
    """为所有蓝图注册中间件"""
    pb_before_request_funcs_map = {}
    pb_after_request_funcs_map = {}
    for bp in blueprint_list:
        pb_before_request_funcs_map[bp.name] = before_request_funcs
        pb_after_request_funcs_map[bp.name] = after_request_funcs
    app.before_request_funcs = pb_before_request_funcs_map
    app.after_request_funcs = pb_after_request_funcs_map


# 允许匿名访问的路径（无需登录）
ALLOW_ANONYMOUS_ACCESS_PATHS = {
    '/api/msg/sendEmail/',
}


def parse_current_request_data(): ...
    # uid = int(request.headers.get(const.REQ_HEADER_KEY_UID, 0))
    # token = str(request.headers.get(const.REQ_HEADER_KEY_TOKEN, ''))
    # user = str(request.headers.get(const.REQ_HEADER_KEY_USER, '{}'))

    # g.uid = uid
    # g.token = token
    # g.user = json.loads(user)


def set_response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cache-Control'] = 'no-store,no-cache'
    return response


# 请求到达 handler 方法前调用
before_request_funcs = [
    parse_current_request_data,
]

# 请求在 handler 方法处理后，响应前调用
after_request_funcs = [
    set_response_headers
]
