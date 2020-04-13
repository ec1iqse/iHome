# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : task_sms.py
@Time    : 2020/4/13 20:47
@Author  : 
@Email   : 
@Desc  :
"""
import os
from celery import Celery
from iHome.libs.yuntongxun.SMS import CCP

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery_app = Celery("iHome", broker="redis://:admin@localhost:6379/1")


@celery_app.task
def send_sms(to, datas, temp_id):
    # 发送短信的异步任务
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)
