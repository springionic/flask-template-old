# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/26
from marshmallow import Schema, fields


class PageSchema(Schema):
    """用于接收验证分页参数的schema"""
    current_page = fields.Int(required=True)
    page_size = fields.Int(required=True)
    filter = fields.Str(required=False, missing='')
    order_by = fields.Str(required=False, missing='id')
    order_rule = fields.Str(required=False, missing='asc')

