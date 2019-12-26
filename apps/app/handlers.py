# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from marshmallow import EXCLUDE, Schema, fields
from sqlalchemy.exc import IntegrityError

from apps.app.schemas import UserSchema
from apps.app.services import UserService
from components import BaseHandler, error_codes, get_logger
from components.error_codes import SERVER_PARAM_INVALID
from components.global_schema import PageSchema
from config.exceptions import BusinessException


log = get_logger('app-handlers')

"""
############################################################
URL               方法         说明                        |
-----------------------------------------------------------|
/users/           GET          给出一个包含所有用户的列表  |
/users/           POST         创建一个新用户              |
/users/<id>/      GET          显示一个用户                |
/users/<id>/      PUT          更新一个用户                |
/users/<id>/      DELETE       删除一个用户                |
-----------------------------------------------------------|
############################################################
"""

class UserHandler(BaseHandler):
    """ handler负责：接收参数和返回参数
        schema负责：接收参数的序列化和返回数据的序列化
        service负责：业务处理，很多复杂业务在service完成
    """

    # 这个schema能用则都复用这一个，否则每个方法里单独创建，具体看需求
    schema = UserSchema(unknown=EXCLUDE, load_only=('is_deleted',))

    service = UserService()

    def get(self, **kwargs):
        id = kwargs.get('id', None)
        if id:
            user = self.service.get_by_id(id)
            if not user:
                raise BusinessException(error_codes.USER_NOT_FOUND)
            return self.success(data={'user': self.schema.dump(user)})
        else:
            req_data = self.get_request_form()
            schema = PageSchema(unknown=EXCLUDE)
            self.validate(schema, req_data)
            pagination_data = schema.load(req_data)
            pagination_users = self.service.list_pagination(pagination_data, model_schema=self.schema)
            return self.success(data=pagination_users)

    def post(self):
        req_data = self.get_request_form()
        self.validate(self.schema, req_data)
        try:
            user = self.service.add(self.schema.load(req_data))
        except IntegrityError as e:
            log.info(str(e))
            raise BusinessException(error_code=error_codes.USER_REPEAT)
        return self.success(data={'user': self.schema.dump(user)})

    def put(self, id):
        req_data = self.get_request_form()
        self.schema.validate(req_data)
        user = self.service.update_user(id, req_data)
        return self.success(data={'user': self.schema.dump(user)})

    def delete(self, id):
        pass






