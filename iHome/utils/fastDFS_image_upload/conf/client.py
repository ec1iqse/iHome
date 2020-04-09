# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : client.py
@Time    : 2020/4/8 23:34
@Author  : 
@Email   : 
@Desc  :
"""
import os
import sys

BASE_DIR = os.path.dirname(__file__)


def get_config_path():
    file_path = os.path.join(BASE_DIR, 'client.conf')
    return file_path
