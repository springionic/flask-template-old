# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from components.bases import BaseModel
from config import db


class User(BaseModel):

    __tablename__ = 'user'

    username = db.Column(db.String(48), nullable=False, comment='用户名')

    def __str__(self):
        return self.username

