# -*- coding: utf-8 -*-
# Created by lilei at 2020/1/17
import enum
import re
from datetime import datetime

from sqlalchemy.ext.declarative.base import declared_attr

from config import db
from config.enums import BaseEnum


class BaseModel(db.Model):
    """模型类基类，抽象类"""
    __abstract__ = True

    @declared_attr
    def __tablename__(self):
        model_name = re.sub('(?<!^)(?=[A-Z])', '_', self.__name__).lower()
        if model_name.endswith('_model'):
            return model_name.replace('_model', '')
        return model_name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    create_time = db.Column(db.DateTime, index=True, nullable=False, server_default=db.text('NOW()'), comment='创建时间')
    update_time = db.Column(db.DateTime, index=True, nullable=False, server_default=db.text('NOW()'), onupdate=datetime.now, comment='更新时间')
    is_deleted = db.Column(db.Boolean, nullable=False, default=False, comment='删除标志')


class IntEnum(db.TypeDecorator):
    """
    int enum  自定义的字段类型
    """

    impl = db.SmallInteger

    def __init__(self, enum_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enum_type = enum_type

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        if isinstance(value, BaseEnum):
            return value.value

        return value

    def process_result_value(self, value, dialect):
        return self._enum_type(value)

    def process_literal_param(self, value, dialect):
        pass

    def python_type(self):
        return type(enum.Enum)