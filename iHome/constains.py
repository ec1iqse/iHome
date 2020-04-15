# -*- coding: utf-8 -*-
"""
@Software Plantform: PyCharm
@File    : constains.py
@Time    : 2020/3/19 18:21
@Author  : 
@Email   : 
@Desc  :保存常量
"""
import os
import sys

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

# FastDFS连接
FAST_DFS_URL = "http://39.106.97.132:8888/"

# FastDFS配置文件目录


# 城区信息的缓存时间：7200秒(两小时)
AREA_INFO_REDIS_CACHE_EXPIRE = 60 * 120

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的redis缓存时间：7200秒(两小时)
HOME_PAGE_DATA_REDIS_EXPIRE = 60 * 120

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 60 * 120
