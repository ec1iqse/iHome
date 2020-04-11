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
from iHome.models import House
from iHome import constains
from iHome import redis_store
from iHome.utils.commons import login_required
from flask import request
from flask import g
from iHome.models import db
from iHome.models import Facility


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


@api.route(rule="/houses/info", methods=["POST"])
@login_required
def save_house_info():
    """保存房屋的基本信息"""
    user_id = g.user_id
    house_data = request.get_json()
    title = house_data.get("title")  # 房屋标题
    price = house_data.get("price")  # 房屋单价
    area_id = house_data.get("area_id")  # 房屋所属城区的编号
    address = house_data.get("address")  # 房屋地址
    room_count = house_data.get("room_count")  # 房屋包含的房间数目
    acreage = house_data.get("acreage")  # 房屋面积
    unit = house_data.get("unit")  # 房屋布局(几室几厅)
    capacity = house_data.get("capacity")  # 房屋容纳人数
    beds = house_data.get("beds")  # 房屋卧床数目
    deposit = house_data.get("deposit")  # 押金
    min_days = house_data.get("min_days")  # 最小入住天数
    max_days = house_data.get("max_days")  # 最大入住天数

    # 校验参数
    if not all(
            [title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断金额是否正确
    try:
        price = int(float(price) * 100)  # 数据库中是以分为单位计算
        deposit = int(float(deposit) * 100)
    except Exception as ex:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断城区id是否存在
    try:
        area = Area.query.get(area_id)
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="数据异常")
    if area in None:
        return jsonify(errno=RET.NODATA, errmsg="城区信息有误")

    # 保存房屋信息
    house = House(
        user_id=user_id,
        area_id=area_id,
        title=title,
        price=price,
        address=address,
        room_count=room_count,
        acreage=acreage,
        unit=unit,
        capacity=capacity,
        beds=beds,
        deposit=deposit,
        min_days=min_days,
        max_days=max_days
    )
    try:
        db.session.add(house)
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="保存数据异常")

    # 处理房屋的设施信息
    facilities_ids = house_data.get("facilitiy")
    # 如果用户勾选了设施信息，再保存数据库
    if facilities_ids:
        # ["7","8"]
        try:
            facilities = Facility.query.fileter(Facility.id.in_(facilities_ids)).all()
        except Exception as ex:
            current_app.logger.error(ex)
            return jsonify(errno=RET.DBERR, errmsg="数据库异常")

        if facilities:
            # 表示有合法的数据
            # 保存设施数据
            house.facilities = facilities  # 解决一对多
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as ex:
        current_app.logger.error(ex)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    # 保存数据成功
    return jsonify(errno=RET.OK, errmsg="OK", data={"house_id": house.id})
