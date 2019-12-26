# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16

from config import ma
from apps.app.models import User


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User


