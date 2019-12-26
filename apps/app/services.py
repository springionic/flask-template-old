# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from apps.app.models import User
from components import BaseService, error_codes
from config.exceptions import BusinessException


class UserService(BaseService):

    def __init__(self):
        super(UserService, self).__init__()
        self.model_cls = User

    def update_user(self, id, user_data: dict):
        user = self.get_by_id(id)
        if not user:
            raise BusinessException(error_codes.USER_NOT_FOUND)
        for k, v in user_data.items():
            setattr(user, k, v)
        return self.update(user)
