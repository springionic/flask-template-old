# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from marshmallow import EXCLUDE, Schema, fields
from sqlalchemy.exc import IntegrityError

from apps.app.schemas import UserSchema
from apps.app.services import UserService
from components import BaseHandler, error_codes, get_logger
from components.error_codes import SERVER_PARAM_INVALID
from config.exceptions import BusinessException


log = get_logger('app-handlers')

class UserHandler(BaseHandler):
    """ handler负责：接收参数和返回参数
        schema负责：接收参数的序列化和返回数据的序列化
        service负责：业务处理，很多复杂业务在service完成
    """
    schema = UserSchema(unknown=EXCLUDE)  # 这个schema能用则都复用这一个，否则每个方法里单独创建，具体看需求

    service = UserService()

    def get(self):
        users = self.service.list_all()
        schema = UserSchema(unknown=EXCLUDE, load_only=('is_deleted',))
        return self.success(data={'users': schema.dump(users, many=True)})

    def post(self):
        request_form = self.get_request_form()
        schema = UserSchema(unknown=EXCLUDE, load_only=('is_deleted',))
        schema.validate(request_form)
        try:
            user = self.service.add(schema.load(request_form))
        except IntegrityError as e:
            log.info(str(e))
            raise BusinessException(error_code=error_codes.USER_REPEAT)
        return self.success(data={'user': schema.dump(user)})

# 对于一个表的增删改查，往往用 => 两条路由，两个类来实现，分别是：
# 获取某一条、获取所以、增加、修改、删除，其中删除为伪删除，和修改类似

class UserHandler2(BaseHandler):

    schema = UserSchema(unknown=EXCLUDE, load_only=('is_deleted',))

    service = UserService()

    def get(self, id):
        user = self.service.get_by_id(id)
        return self.success(data={'user': self.schema.dump(user)})

    def put(self, id):
        req_data = self.get_request_form()
        self.schema.validate(req_data)
        user = self.service.update_user(id, req_data)
        return self.success(data={'user': self.schema.dump(user)})

    def delete(self, id):
        pass


