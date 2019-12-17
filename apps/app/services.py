# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from apps.app.models import User
from components import BaseService


class UserService(BaseService):

    def __init__(self):
        super(UserService, self).__init__()
        self.model_cls = User

    def update_user(self, id, req_data):
        user = self.session.query(self.model_cls).filter_by(id=id)
        user['username'] = req_data['username']
        return self.update(user)
