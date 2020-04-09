# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : houses.py
@Time    : 2020/4/9 10:39
@Author  : 
@Email   : 
@Desc  :
"""
import json
from . import api
from flask import jsonify
from iHome.utils.response_code import RET
from flask import current_app
from iHome.models import Area
from iHome import constains
from iHome import redis_store


@api.route(rule="/areas", methods=["GET"])
def get_area_info():
    """获取城区信息"""

    # 尝试从redis中读取数据

    try:
        resp_json = redis_store.get("area_info")
    except Exception as ex:
        current_app.logger.error(ex)
    else:
        if resp_json is not None:
            # redis存在缓存数据
            current_app.logger.info("hit redis area_info")
            return resp_json, 200, {"Content-Type": "application/json"}

    # 查询数据库，读取程序信息
    try:
        area_list = Area.query.all()
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    area_dict_li = []

    # 将对象转换为字典
    for area in area_list:
        area_dict_li.append(area.to_dict())

    # 将数据转换为json字符串
    resp_dict = dict(errno=RET.OK, errmsg="OK", data=area_dict_li)
    resp_json = json.dumps(resp_dict)

    # 将数据保存到redis中
    try:
        redis_store.setex("area_info", constains.AREA_INFO_REDIS_CACHE_EXPIRE, resp_json)
    except Exception as ex:
        current_app.logger.error(ex)

    return resp_json, 200, {"Content-Type": "application/json"}
