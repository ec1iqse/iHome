# -*- coding: utf-8 -*-
"""
@Software Plantform: PyCharm
@File    : verify_code.py
@Time    : 2020/3/19 0:54
@Author  : 
@Email   : 
@Desc  :
"""
from . import api
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store
from iHome import constains
from flask import current_app
from flask import jsonify
from iHome.utils.response_code import RET
from flask import make_response
from flask import request
from iHome import db
from iHome.models import User
from random import randint
from iHome.libs.yuntongxun.SMS import CCP


# 定义视图
#  get: localhost/api/v1.0/image_codes/<image_code_id>
@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取验证码图片
    :param image_code_id:图片验证码编号
    :return: 正常情况下返回的是验证码图片，出现异常时返回json
    """

    # 获取参数

    # 校验参数

    # 业务逻辑处理
    # 生成验证码图片
    # 名字 真实文本 图片数据
    name, text, image_data = captcha.generate_captcha()
    # 将验证码真实值与编号保存到Redis中,并设置有效期

    # redis数据类型：字符串 列表 哈希 集合 有序集合

    # "key":value
    # "image_code":{"编号1"真实文本","编号2":"真实文本"}:
    # hset("image_code","id1",)
    # 使用hash维护有效期的时候只能整体设置

    # 单条维护记录选用字符串类型
    # "image_code_编号1":"真实值"
    # "image_code_编号2":"真实值"
    try:
        #                            记录名字                                 有效期                             值
        redis_store.setex(name="image_code_{}".format(image_code_id), time=constains.IMAGE_CODE_REDIS_EXPIRE,
                          value=text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        # return jsonify(errno=RET.DBERR, errmsg="save image code failed")
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码失败")

    # redis_store.set("image_code_{}".format(image_code_id), text)
    # redis_store.exipre("image_code_{}".format(image_code_id), constains.IMAGE_CODE_REDIS_EXPIRE)

    # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
    # 返回值


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxxx
@api.route("/sms_codes/<regex(r'1[3-9]\d{9}'):mobile>", )
def get_sms_code(mobile):
    """获取短信验证码"""
    print(mobile)

    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    # 校验参数

    if not all([image_code, image_code_id]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理

    # 从redis中提取真实的图片验证码
    try:
        real_image_code = redis_store.get("image_code_{}".format(image_code_id)).decode("UTF-8")
    except Exception as  ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")

    print("验证码", image_code)
    print("真实验证码", real_image_code)

    # 判断验证码是否过期
    if real_image_code is None:
        # 图片验证码或过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    print("验证码", image_code.lower())
    print("真实验证码", real_image_code.lower())

    # 判断用户输入的验证码是否正确
    if real_image_code.lower() != image_code.lower():
        # 用户输入的验证码错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 进行对比与用户填写的值

    # 判断手机号是否已经注册
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as ex:
        current_app.logger.error(ex)
    else:
        if user is not None:
            # 手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    # 如果手机号不存在，则生成短信验证码(6位整数)
    sms_code = "%06d" % randint(0, 999999)

    # 保存真实验证码
    try:
        redis_store.setex("sms_code_{}".format(mobile), constains.SMS_CODE_REDIS_EXPIRE, sms_code)
    except Exception as ex:
        current_app.logger.error(ex)

        return jsonify(error=RET.DBERR, errmsg="保存短信验证码异常")
    # 发送短信
    ccp = CCP()
    try:
        result = ccp.send_template_sms(to=mobile, datas=[sms_code, int(constains.SMS_CODE_REDIS_EXPIRE / 60)],
                                       temp_id=1)
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(error=RET.THIRDERR, errmsg="发送异常")

    # ccp.send_template_sms(mobile, [sms_code,int(constains.SMS_CODE_REDIS_EXPIRE / 60)],1)
    if result == 0:
        # 发送成功
        return jsonify(error=RET.OK, errmsg="发送成功")
    else:
        return jsonify(error=RET.THIRDERR, errmsg="第三方发送失败")
    # 返回值
