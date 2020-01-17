# -*- coding: utf-8 -*-
# Created by lilei at 2020/1/17
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import Schema

from config import error_codes
from config.exceptions import CommonException


class BaseHandler(MethodView):
    """所有handler处理类的基类"""

    schema = None

    service = None

    def __init__(self):
        # 包含所有请求参数，不推荐在 handler 和 service 中使用此属性，适用于调试、打印日志等
        self.req_form = self.get_request_form()

        # 如果请求有 req_schema，则此值为 req_schema 严格 dump 出来的值
        # 否则，此值和 req_form 相等
        """
        self.req_form_strict = self.req_form

        # 当 handler 未指定 req_schema 时，读取请求 handler 对应子类 schema，并设置为当前请求 handler 的 req_schema
        # 当 handler 指定 req_schema 时，优先使用指定的 schema，即使为 None
        if not hasattr(self, 'req_schema'):
            for _, v in self.__class__.__dict__.items():
                if type(v) == type(Schema):
                    self.req_schema = v
                    break

        # 如果存在 req_schema，使用 req_schema 校验请求参数 req_form
        if hasattr(self, 'req_schema') and self.req_schema:
            req_schema = self.req_schema(unknown=EXCLUDE)
            self.validate(req_schema, self.req_form)
            self.req_form_strict = req_schema.load(self.req_form)
        """

    @staticmethod
    def get_request_form():
        if request.method == 'GET':
            return request.args.to_dict(flat=True)
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if not request.is_json:
                raise CommonException(error_code=error_codes.SERVER_PARAM_INVALID)
            return request.get_json()
        return {}

    @staticmethod
    def validate(schema: Schema, data):
        error_msgs = schema.validate(data)
        if not error_msgs:
            return
        if '_schema' in error_msgs and error_msgs['_schema']:
            msg = ', '.join(error_msgs['_schema'])
            raise CommonException(error_code=error_codes.SERVER_PARAM_INVALID, msg=msg)

        raise CommonException(error_code=error_codes.SERVER_PARAM_INVALID, data=error_msgs)

    @staticmethod
    def success(message='OK!', data=None):
        result = {
            'msg': message
        }
        # 不返回数据
        if not data:
            return jsonify(result), 200
        # 返回 list 数据
        if isinstance(data, list):
            result['data'] = {
                'list': data
            }
        else:
            # 返回 dict 数据
            result['data'] = data
        return jsonify(result), 200

    @staticmethod
    def fail(error_code, data=None):
        result = {
            'msg': error_code[1]
        }
        if data:
            result['data'] = data
        return jsonify(result), error_code[0]