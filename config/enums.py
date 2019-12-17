# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16

from enum import Enum, unique


@unique
class BaseEnum(Enum):
    @classmethod
    def has_value(cls, value):
        """
        判断枚举类型是否包含枚举值 value
        :param value: 枚举值
        :return: True or False
        """
        return any(value == item.value for item in cls)

    @classmethod
    def value_list(cls):
        """
        值列表
        :return: tuple
        """
        return [item.value for item in cls]


class UserSexEnum(BaseEnum):
    """
    用户性别枚举
    """
    UNKNOWN = 0  # 未知
    MALE = 1  # 男
    FEMALE = 2  # 女