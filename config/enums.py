# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from bases.base_enum import BaseEnum


class UserSexEnum(BaseEnum):
    """
    用户性别枚举
    """
    UNKNOWN = 0  # 未知
    MALE = 1  # 男
    FEMALE = 2  # 女