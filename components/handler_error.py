# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound, InternalServerError

from components import error_codes, BaseHandler, get_logger
from config.exceptions import MyBaseException


HTTP_EXCEPTION_ERROR_CODE_MAP = {
    MethodNotAllowed: error_codes.SERVER_METHOD_NOT_ALLOWED,
    BadRequest: error_codes.SERVER_BAD_REQUEST,
    NotFound: error_codes.SERVER_PATH_NOT_FOUND
}

error_logger = get_logger('components-error')


def error_handler(e):
    """
    全局异常处理
    """
    if isinstance(e, MyBaseException):  # 自定义的一些错误
        print(e)
        error_code = (getattr(e, 'code'), getattr(e, 'msg'))
        data = getattr(e, 'data', None)
        return BaseHandler.fail(error_code, data)

    error_code = HTTP_EXCEPTION_ERROR_CODE_MAP.get(type(e))
    # if isinstance(e, ValidationError):  # 反序列化参数出错
    #     error_code = (412, str(e))
    if isinstance(e, AssertionError):  # 某些地方 assert 出错
        error_code = (400, str(e))
    if not error_code:  # 未知服务器内部代码错误
        error_code = error_codes.SERVER_INTERVAL_ERROR
        error_logger.exception(e)

    return BaseHandler.fail(error_code)
