# -*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config_map
from iHome.utils.commons import RegexConverter

# 数据库
db = SQLAlchemy()

# 创建Redis连接对象
redis_store = None
redis_pool = None

# 为flask补充CSRF防护机制
# csrf = CSRFProtect()

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级

# 创建日志记录器，指明日志保存的路径，每个日志文件的最大大小，保存的日志文件个数上限
file_log_handler = RotatingFileHandler(filename="logs/log",
                                       maxBytes=1024 * 1024 * 100,
                                       backupCount=10,
                                       encoding="utf-8",
                                       delay=False)

# 创建日志记录格式               日志等级       日志信息的文件名 行数        日志信息
formatter = logging.Formatter("%(levelname)s - %(filename)s - %(lineno)s - %(message)s")

# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)

# 为全局的日志工具对象(Flask app使用的)添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(mode="develop"):
    """
    创建flask的应用对象
    :param mode:str 配置模式的名称("develop","product",默认是develop)
    :return:
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(mode)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 初始化Redis
    global redis_pool
    global redis_store
    redis_pool = redis.ConnectionPool(host=config_class.REDIS_HOST,
                                      port=config_class.REDIS_PORT,
                                      password=config_class.REDIS_PASSWORD,
                                      max_connections=config_class.REDIS_MAX_CONNECTIONS)

    # redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT,
    #                                 password=config_class.REDIS_PASSWORD)

    redis_store = redis.StrictRedis(connection_pool=redis_pool)

    # 为Flask补充CSRF防护
    # csrf.init_app(app=app)

    # 利用Flask-Session将Session保存到Redis
    Session(app=app)

    # 为flask添加自定义转换器
    app.url_map.converters['regex'] = RegexConverter

    # 注册蓝图
    from iHome import api_1_0  # 推迟导入

    app.register_blueprint(blueprint=api_1_0.api, url_prefix="/api/v1.0")

    # 注册提供静态文件的蓝图
    from iHome.web_html import html
    app.register_blueprint(blueprint=web_html.html)
    return app
