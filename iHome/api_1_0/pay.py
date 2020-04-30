# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : pay.py
@Time    : 2020/5/1 0:39
@Author  : 
@Email   : 
@Desc  :
"""
import os
from . import api
from iHome.utils.commons import login_required
from iHome.models import Order
from flask import g
from flask import current_app
from flask import jsonify
from iHome.utils.response_code import RET
from alipay import AliPay, DCAliPay, ISVAliPay
from iHome import constains


@api.route(rule="/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
    """发起支付宝支付"""
    user_id = g.user_id
    # 判断订单状态
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id, Order.status == "WAIT_PAYMENT").first
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if order is None:
        return jsonify(errno=RET.NODATA, errmsg="订单数据有误")

    # 创建支付宝的sdk对象
    alipay_client = AliPay(
        appid="2016102400753059",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单编号
        total_amount=order.amount / 100.0,  # 金额
        subject=f"爱家租房 {order.id}",  # 订单标题
        return_url="http://localhost:5000/orders.html",  # 返回的连接地址
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 让用户跳转的支付宝链接地址
    pay_url = constains.ALIPAY_URL_PREFIX + order_string

    return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})
