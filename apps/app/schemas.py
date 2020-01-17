# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from marshmallow import Schema, fields


class TestScheme(Schema):

    project_id = fields.Int(required=True, missing=0, default=0)
    name = fields.Str(required=True)
    friends = fields.List(fields.String(), required=True)

