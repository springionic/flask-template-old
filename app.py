# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from flask import Flask

from components.handler_error import error_handler
from components.middlewares import register_middleware
from config import Config, db, ma, search
from routes import blueprint_list


def create_app() -> Flask:
    # 返回全局的Flask对象
    app = Flask(__name__, template_folder=None, static_folder=None)  # Flask对象

    app.config.from_object(Config)  # 添加配置信息

    search.init_app(app)  # 全文搜索插件
    db.init_app(app)  # SQLAlchemy对象初始化Flask对象
    ma.init_app(app)  # marshmallow初始化Flask对象
    app.register_error_handler(Exception, error_handler)  # 注册异常
    register_middleware(app)  # 注册中间件
    [app.register_blueprint(blueprint) for blueprint in blueprint_list]  # 注册所有蓝图

    return app

# 导入模型，才能迁移
from apps.app.models import User

