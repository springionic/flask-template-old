# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16

from flask import Blueprint

from apps.app.handlers import *

app_blueprint = Blueprint('app', __name__, url_prefix='/app')


app_blueprint.add_url_rule('/user/',
                           view_func=UserHandler.as_view('user'), methods=['GET', 'POST'])
app_blueprint.add_url_rule('/user/<int:id>/',
                           view_func=UserHandler.as_view('user-api'), methods=['GET', 'PUT', 'DELETE'])
