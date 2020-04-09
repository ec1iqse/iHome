# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : profile.py
@Time    : 2020/4/5 16:31
@Author  : 
@Email   : 
@Desc  :
"""
from . import api
from iHome.utils.commons import login_required
from flask import jsonify
from flask import g
from flask import request
from iHome.utils.response_code import RET
import imghdr
from iHome.utils.FastDFS_image_upload.image_storage import upload_image_by_buffer

from flask import current_app
from iHome.models import User
from iHome import db
from iHome import constains
from flask import session


@api.route(rule="/users/avatar", methods=["POST"])
@login_required
def set_user_avatar():
    print("设置用户头像")

    """设置用户的头像
    参数：图片(多媒体表单)，用户ID

    """
    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id
    # 获取图片
    image_file = request.files.get("avatar")
    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")
    try:
        file_name = upload_image_by_buffer(file_buffer=image_file)
    except Exception as ex:
        print(ex)
        current_app.logger.error(ex)
        return jsonify(errno=RET.THIRDERR, errmsg="图片上传失败")

    # 保存文件名到数据库中
    try:
        User.query.filter_by(id=user_id).update({
            "avatar_url": file_name
        })
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="保存图片信息失败")

    # 保存成功返回
    avatar_url = constains.FAST_DFS_URL + file_name

    return jsonify(errno=RET.OK, errmsg="保存成功", data={
        "avatar_url": avatar_url
    })


@api.route(rule="/users/name", methods=["PUT"])
@login_required
def change_user_name():
    """修改用户名"""
    user_id = g.user_id

    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    name = req_data.get("name")
    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg="名字不能为空")

    # 保存用户昵称name,并同时判断name是否重复(利用数据库的唯一索引)
    try:
        User.query.filter_by(id=user_id).update({"name": name})
        db.session.commit()
    except Exception as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="设置用户错误")

    # 修改session数据中的name字段
    session["name"] = name
    return jsonify(errno=RET.OK, errmsg="OK", data={"name": name})


@api.route(rule="/user", methods=["GET"])
@login_required
def change_user_name():
    """获取个人信息"""
    user_id = g.user_id
    # 查询数据库获取个人信息
    try:
        user = User.query.get(user_id)
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")
    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())


@api.route(rule="/users/auth", methods=["GET"])
@login_required
def get_user_auth():
    """获取用户实名认证信息"""
    user_id = g.user_id
    # 在数据库中查询信息
    try:
        user = User.query.get(user_id)
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="获取用户实名信息失败")
    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")
    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())


@api.route(rule="/users/auth", methods=["POST"])
@login_required
def set_user_auth():
    """保存实名认证信息"""
    user_id = g.user_id

    # 获取参数
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    real_name = req_data.get("real_name")
    id_card = req_data.get("id_card")

    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None).update(
            {"real_name": real_name, "id_card": id_card})
        db.session.commit()
    except Exception as ex:
        current_app.error(ex)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存用户实名信息失败")
    return jsonify(errno=RET.OK, errmsg="OK")
