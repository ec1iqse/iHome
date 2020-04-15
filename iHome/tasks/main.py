# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : main.py
@Time    : 2020/4/14 21:38
@Author  : 
@Email   : 
@Desc  :
"""
import os
from celery import Celery
from iHome.tasks import config

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# # 定义celery对象
celery_app = Celery("iHome")
# # 引入配置信息
celery_app.config_from_object(config)
# # 自动搜寻异步任务
celery_app.autodiscover_tasks(packages=["iHome.tasks.sms"])