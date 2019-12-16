# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config.env import *


class Config(object):
    # flask添加的配置对象
    DEBUG = DEBUG_STATUS
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}'.format(
        username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db=DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()  # 数据库连接对象
ma = Marshmallow()  # 序列化对象