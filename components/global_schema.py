# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/26
from marshmallow import Schema, fields

from config import ma

from apps.app.models import User


class PageSchema(Schema):
    """用于接收验证分页参数的schema"""
    current_page = fields.Int(required=True, data_key='current_page')
    page_size = fields.Int(required=True, data_key='page_size')
    filter = fields.Str(required=False, missing='', data_key='filter')
    order_by = fields.Str(required=False, missing='id', data_key='order_by')
    order_rule = fields.Str(required=False, missing='asc', data_key='order_rule')


class UserSchema(ma.ModelSchema):
    """用户表的schema"""
    class Meta:
        model = User
        included_fk = True  # 包括外键
