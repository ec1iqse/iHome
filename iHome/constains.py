# -*- coding: utf-8 -*-
"""
@Software Plantform: PyCharm
@File    : constains.py
@Time    : 2020/3/19 18:21
@Author  : 
@Email   : 
@Desc  :保存常量
"""

# 图片验证码有效期(Redis) 3*60=180秒
IMAGE_CODE_REDIS_EXPIRE = 3 * 60

# 短信验证码有效期(Redis) 5*60=300秒
SMS_CODE_REDIS_EXPIRE = 5 * 60

# 发送短信验证码间隔(Redis) 1*60=60秒
SEND_SMS_CODE_INTERVAL = 1 * 60

# 登录错误尝试次数
LOGIN_ERROR_MAX_TIMES = 5

# 登录错误限制时间 单位：10*60=600秒
LOGIN_ERROR_FORBID_TIME = 60 * 10
