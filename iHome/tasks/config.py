# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : config.py
@Time    : 2020/4/14 21:47
@Author  : 
@Email   : 
@Desc  :
"""
BROKER_URL = "redis://:admin@127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "redis://:admin@127.0.0.1:6379/2"
