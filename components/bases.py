# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
import re
from ast import literal_eval
from datetime import datetime

from flask import request, jsonify
from flask.views import MethodView
from marshmallow import Schema
from sqlalchemy import desc
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Query

from components.pagination import Pagination
from bases.singleton import Singleton
from config import db, search, error_codes
from config.exceptions import CommonException


IS_DELETED_COLUMN_NAME = 'is_deleted'


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


class BaseService(object, metaclass=Singleton):
    """所有service服务类的基类"""
    def __init__(self):
        self.model_cls = None

    @property
    def query(self):
        return Query(self.model_cls, self.session)

    @property
    def session(self):
        session = db.session
        return session

    def _get(self, column_name: str, value, include_deleted_item: bool = False, only_one: bool = True):
        """
        获取数据
        :param column_name: 列名称
        :param value: 列对应的检索值
        :param include_deleted_item: 是否包含已删除的项目(is_deleted = True); True: 包含; False: 不包含;
        :param only_one: 查询结果集是否仅一项; True: 仅一个符合条件的结果; False: 所有符合条件的结果;
        :return:
        """
        query = self.session.query(self.model_cls).filter(getattr(self.model_cls, column_name) == value)
        # 如果有 is_deleted 列
        if hasattr(self.model_cls, IS_DELETED_COLUMN_NAME) and not include_deleted_item:
            query = query.filter_by(is_deleted=False)
        return query.first() if only_one else query.all()

    def get(self, column_name: str, value, include_deleted_item: bool = False):
        return self._get(column_name, value, include_deleted_item)

    def get_by_id(self, value: int, include_deleted_item: bool = False):
        return self.get('id', value, include_deleted_item)

    def list(self, column_name: str, value, include_deleted_item: bool = False):
        return self._get(column_name, value, include_deleted_item, only_one=False)

    def list_all(self):
        return self.session.query(self.model_cls).all()

    def list_pagination_new(self, page_data: dict, model_schema: Schema) -> dict:
        # 新版分页查询，比下边的要更佳
        current_page = page_data.get('current_page', 1)  # 当前页
        page_size = page_data.get('page_size', 10)  # 每页大小
        filter = page_data.get('filter', '')  # 过滤条件
        order_by = page_data.get('order_by', 'id')  # 排序字段
        order_rule = page_data.get('order_rule', 'asc')  # 排序规则
        # 全文检索插件进行搜索，改变原来的
        if order_rule != 'desc':
            pagination = search.msearch(self.model_cls, query=filter) \
                .order_by(order_by) \
                .paginate(current_page, page_size)
        else:
            pagination = search.msearch(self.model_cls, query=filter) \
                .order_by(desc(order_by)) \
                .paginate(current_page, page_size)

        return {
            'list': model_schema.dump(pagination.items, many=True) ,
            'current_page': pagination.page,
            'total': len(pagination.items),  # 这里有问题可能，可以不需要也
            'page_total': pagination.pages,
            'page_size': page_size
        }


    def list_pagination(self, page_data: dict, model_schema: Schema) -> dict:
        # 这里的分页操作最好用Flask自带的paginate来完成
        # items = self.session.query(self.model_cls) \
        #     .filter(*filters) \
        #     .order_by(*order_bys) \
        #     .limit(page_size).offset((current_page - 1) * page_size) \
        #     .all()

        current_page = page_data.get('current_page', 1)  # 当前页
        page_size = page_data.get('page_size', 10)  # 每页大小
        filter = page_data.get('filter', '')  # 过滤条件
        order_by = page_data.get('order_by', 'id')  # 排序字段
        order_rule = page_data.get('order_rule', 'asc')  # 排序规则
        # 全文检索插件进行搜索，改变原来的
        if order_rule != 'desc':
            items = search.msearch(self.model_cls, query=filter) \
                .order_by(order_by) \
                .limit(page_size).offset((current_page-1) * page_size)
        else:
            items = search.msearch(self.model_cls, query=filter) \
                .order_by(desc(order_by)) \
                .limit(page_size).offset((current_page - 1) * page_size)

        if current_page == 1 and len(list(items)) < page_size:
            total = len(list(items))
        else:
            # total = self.session.query(self.model_cls).filter(*filters).order_by(*order_bys).count()
            total = search.msearch(self.model_cls, query=filter).count()
        pagination_info = literal_eval(str(Pagination(current_page, page_size, total, items)))  # 获取分页状况信息
        items = model_schema.dump(items, many=True)  # 查询对象列表
        # table_plural = self.model_cls.__tablename__ + 's'  # 表名复数
        pagination_info['list'] = items  # 合并信息

        return pagination_info

    def add(self, instance):
        session = self.session
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def update(self, instance):
        session = self.session
        instance = session.merge(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def delete(self, id):
        instance = self.get_by_id(id)
        instance.is_deleted = True
        self.session.commit()
        self.session.refresh()
        return instance


class BaseModel(db.Model):
    """模型类基类，抽象类"""
    __abstract__ = True

    @declared_attr
    def __tablename__(self):
        model_name = re.sub('(?<!^)(?=[A-Z])', '_', self.__name__).lower()
        if model_name.endswith('_model'):
            return model_name.replace('_model', '')
        return model_name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    create_time = db.Column(db.DateTime, index=True, nullable=False, server_default=db.text('NOW()'), comment='创建时间')
    update_time = db.Column(db.DateTime, index=True, nullable=False, server_default=db.text('NOW()'), onupdate=datetime.now, comment='更新时间')
    is_deleted = db.Column(db.Boolean, nullable=False, default=False, comment='删除标志')


