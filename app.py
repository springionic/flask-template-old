# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from flask import Flask

from components.error import error_handler
from config import Config, db, ma
from routes import blueprint_list


def create_app() -> Flask:
    # 返回全局的Flask对象
    app = Flask(__name__, template_folder=None, static_folder=None)  # Flask对象

    app.config.from_object(Config)  # 添加配置信息

    db.init_app(app)  # SQLAlchemy对象初始化Flask对象
    ma.init_app(app)  # marshmallow初始化app
    app.register_error_handler(Exception, error_handler)  # 注册异常

    # 注册所有蓝图
    for blueprint in blueprint_list:
        app.register_blueprint(blueprint)

    return app

# 导入模型，才能迁移
from apps.app.models import User

