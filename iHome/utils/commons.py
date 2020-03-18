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
class ReConverter(BaseConverter):
    """实现"""

    def __init__(self, url_map, regex):
        # 调用父类方法
        super(ReConverter, self).__init__(map=url_map)
        # 保存正则表达式
        self.regex = regex
