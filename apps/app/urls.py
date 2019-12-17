# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16

from flask import Blueprint
from flask_restful import Api

from apps.app.handlers import *

app_blueprint = Blueprint('app', __name__, url_prefix='/app')
app_api = Api(app_blueprint)


app_api.add_resource(UserHandler, '/user/', endpoint='user')
app_api.add_resource(UserHandler2, '/user/<int:id>/', endpoint='user2')