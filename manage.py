# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16

from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from config import db


app = create_app()  # 返回的全局app对象

manager = Manager(app)  # 管理

migrate = Migrate(app, db)  # 迁移

def make_shell_context():  # shell
    return dict(app=app)

manager.add_command('runserver', Server(host='127.0.0.1', port=5000, use_debugger=True, use_reloader=True))
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# 项目启动
if __name__ == '__main__':
    manager.run(default_command='runserver')