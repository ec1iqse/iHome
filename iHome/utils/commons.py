# -*- coding: utf-8 -*-
"""
@Software: PyCharm
@File    : commons.py
@Time    : 2020/3/18 15:50
@Author  : 
@Email   : 
@Desc  :
"""
from werkzeug.routing import BaseConverter
from flask import session
from iHome.utils.response_code import RET
from flask import jsonify
from flask import g
import functools


# 定义正则转换器
class RegexConverter(BaseConverter):

    def __init__(self, url_map, *args):
        # 调用父类方法
        super(RegexConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = args[0]


# 定义的验证登录状态的装饰器
def login_required(view_func):
    # @functools.wraps将原函数对象的指定属性复制给包装函数对象
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        # 如果用户是登录的,执行视图函数
        user_id = session.get("user_id")
        if user_id is not None:
            # 将user_id保存到g对象中，在视图函数中可以通过g对象获取保存数据
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            # 如果未登录，返回未登录的信息
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return wrapper


# @login_required
# def set_user_avatar():
#     user_id = g.user_id
#     pass
