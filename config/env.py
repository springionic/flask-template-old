# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
import os
from ast import literal_eval

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 以下配置均从环境变量中获取
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')  # 数据库主机地址

DB_PORT = int(os.getenv('DB_PORT', 3306))  # 数据库端口

DB_USERNAME = os.getenv('DB_USERNAME', 'root')  # 数据库用户名

DB_PASSWORD = os.getenv('DB_PASSWORD', 'lilei120400')  # 数据库密码

DB_NAME = os.getenv('DB_NAME', 'flask_test')  # 数据库库名

DEBUG_STATUS = literal_eval(os.getenv('DEBUG', 'true').capitalize())  # 调试模式

LOG_DIR = os.getenv('LOG_DIR', os.path.join(BASE_DIR, 'logs'))  # 日志目录



