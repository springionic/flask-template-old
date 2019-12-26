import os

import flask
import pytest  # type: ignore
from flask.testing import FlaskClient

from components.handler_error import error_handler
from manage import app as _app
from config import db as _db
from run import before_request_funcs, bp_list
from run import after_request_funcs  # type: ignore



CUR_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    _app.config['TESTING'] = True
    _app.config['SERVER_NAME'] = "127.0.0.1"

    # _app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:@localhost:5432/longleding_test'
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:lilei120400@localhost:5432/verify3_test'
    # _app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lilei120400@localhost:3306/verify3_test'
    # _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(CUR_DIR, 'test.db')
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()
    def teardown():
        ctx.pop()
    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    def teardown():
        _db.session.commit()
        _db.drop_all()
    _db.app = app
    _db.create_all()
    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="session")
def client(app, db):
    with app.test_client() as client:
        yield client


headers = {"X-YL-Uid": 99, "X-YL-User": '{"name":"pm","id":99}'}  # 测试请求头

project_id = 88  # 测试项目id
center_id = 256


def http_req(client: FlaskClient, url: str, method: str, payload: dict) -> dict:
    """
    发送测试请求
    :param client: flask客户端对象
    :param url: 路由
    :param method: 请求方法
    :param payload: 参数
    :return: 数据
    """
    if method.upper() == 'GET':
        return client.get(url, query_string=payload).json
    if method.upper() == 'POST':
        return client.post(url, json=payload, headers=headers).json
    if method.upper() == 'PUT':
        return client.put(url, json=payload, headers=headers).json
    if method.upper() == 'DELETE':
        return client.delete(url, json=payload, headers=headers).json
    if method.upper() == 'PATCH':
        return client.patch(url, json=payload, headers=headers).json
    else:
        raise RuntimeError('Http method error!')
