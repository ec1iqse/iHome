# -*- coding: utf-8 -*-
"""
@Software: PyCharm
@File    : commons.py
@Time    : 2020/3/18 15:50
@Author  : 
@Email   : 
@Desc  :
"""
from werkzeug.routing import BaseConverter


# 定义正则转换器
class RegexConverter(BaseConverter):

    def __init__(self, url_map, *args):
        # 调用父类方法
        super(RegexConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = args[0]
