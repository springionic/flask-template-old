# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from apps.app.schemas import UserSchema
from apps.app.services import UserService
from components import BaseHandler



class UserHandler(BaseHandler):
    """ handler负责：接收参数和返回参数
        schema负责：接收参数的序列化和返回数据的序列化
        service负责：业务处理
    """
    schema = UserSchema()

    service = UserService()

    def get(self):
        users = self.service.get_users()
        return self.success(data={'users': self.schema.dump(users, many=True)})

    def post(self):
        request_form = self.get_request_form()
        self.schema.validate(self.UserSchema, partial=('username'))
        user = self.service.add_user(request_form['username'])
        return {'data': {'user': self.schema.dump(user)}}




