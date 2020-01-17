# -*- coding: utf-8 -*-
# Created by lilei at 2020/1/17
from ast import literal_eval

from marshmallow import Schema
from sqlalchemy import desc
from sqlalchemy.orm import Query

from bases.singleton import Singleton
from components.pagination import Pagination
from config import db, search


IS_DELETED_COLUMN_NAME = 'is_deleted'

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