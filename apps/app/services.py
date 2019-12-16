# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from apps.app.models import User
from components import BaseService


class UserService(BaseService):

    def __init__(self):
        super(UserService, self).__init__()
        self.model_cls = User

    def get_users(self):
        return self.list_all()

    def add_user(self, username):
        user = User(username=username)
        user = self.add(user)
        return user