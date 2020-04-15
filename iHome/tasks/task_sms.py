# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : task_sms.py
@Time    : 2020/4/13 20:47
@Author  : 
@Email   : 
@Desc  :
"""
from iHome.libs.yuntongxun.SMS import CCP
from iHome.tasks.main import celery_app


@celery_app.task
def send_sms(to, datas, temp_id):
    # 发送短信的异步任务
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)
