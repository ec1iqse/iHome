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


@api.route("/users/avatar", methods=["POST"])
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
