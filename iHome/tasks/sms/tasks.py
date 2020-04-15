# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : tasks.py
@Time    : 2020/4/14 21:39
@Author  : 
@Email   : 
@Desc  :
"""
from iHome.tasks.main import celery_app
from iHome.libs.yuntongxun.SMS import CCP


@celery_app.task
def send_sms(to, datas, temp_id):
    # 发送短信的异步任务
    ccp = CCP()
    ret = ccp.send_template_sms(to, datas, temp_id)
    return ret
