# -*- coding:utf-8 -*-
from flask import Blueprint

# 创建蓝图对象
api = Blueprint("apt_1_0", __name__)

# 导入蓝图视图函数
from . import demo
from . import verify_code
from . import passport
from . import profile
