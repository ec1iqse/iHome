# -*- coding: utf-8 -*-
"""
@Software Plantform: PyCharm
@File    : passport.py
@Time    : 2020/3/29 16:37
@Author  : 
@Email   : 
@Desc  :
"""
import re
from . import api
from flask import request
from flask import jsonify
from iHome.utils.response_code import RET
from iHome import redis_store
from flask import current_app
from iHome.models import User
from iHome.models import db
from sqlalchemy.exc import IntegrityError
from flask import session
from iHome import constains


@api.route(rule="/users", methods=["POST"])
def register():
    """用户注册
    请求的参数：手机号，短信验证码，密码，确认密码
    参数各式：json
    """
    # 获取请求的json数据，返回字典
    request_dict = request.get_json()

    # 获取参数
    mobile = request_dict.get("mobile")
    sms_code = request_dict.get("sms_code")
    password = request_dict.get("password")
    password2 = request_dict.get("password2")

    print("手机号", mobile)
    print("验证码", sms_code)
    print("密码", password)
    print("确认密码", password2)

    # 校验参数
    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[3-9]\d{9}", mobile):
        # 格式不对
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    if password != password2:
        # 两次密码不一致
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")

    # 从Redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_{}".format(mobile))
        if real_sms_code is not None:
            real_sms_code = redis_store.get("sms_code_{}".format(mobile)).decode("UTF-8")
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码失效")

    # 判断用户填写的短信验证码的正确性

    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    # 删除Redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_{}".format(mobile))
    except Exception as ex:
        current_app.logger.error(ex)

    # 判断用户的手机号是否注册过

    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as ex:
    #     current_app.logger.error(ex)
    #     return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    # else:
    #     if user is not None:
    #         # 手机号已存在
    #         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 保存的用户的数据到数据库中
    user = User(name=mobile, mobile=mobile)
    # user.generate_password_hash(origin_password=password)
    user.password = password  # 设置属性

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as ie:
        # 事务回滚
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已经注册过
        current_app.logger.error(ie)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    # 保存登录状态到Session中
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id

    # 返回结果
    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route(rule="/sessions", methods=["POST"])
def login():
    """用户登录
    参数：手机号，密码 json
    """
    # 获取参数
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    # 校验参数
    # 参数完整性
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断手机号各式
    if not re.match(r"1[3-9]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    # 用户的IP地址
    ip = request.remote_addr

    # 判断错误次数是否超过限制,如果超过限制,则返回
    # redis记录:"access_nums_请求的IP地址":次数
    try:
        access_nums = redis_store.get("access_nums_{}".format(ip))
        if access_nums is not None:
            access_nums = redis_store.get("access_nums_{}".format(ip)).decode("UTF-8")
    except Exception as ex:
        current_app.logger.error(ex)

    else:
        print("获得值*****************",access_nums)
        if access_nums is not None and int(access_nums) >= constains.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    # 从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    if user is None or not user.check_password(password=password):
        # 如果验证失败，记录错误次数，返回信息
        try:
            redis_store.incr("access_nums_{}".format(ip))
            redis_store.expire("access_nums_{}".format(ip), constains.LOGIN_ERROR_FORBID_TIME)
        except Exception as ex:
            current_app.logger.error(ex)

        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="登录成功")



@api.route(rule="/session", methods=["GET"])
def check_login():
    # 尝试从session中获取用户的名字
    name = session.get("name")

    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route(rule="/session", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")
