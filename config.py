# -*- coding:utf-8 -*-
import redis


class Config(object):
    """配置信息"""

    SECRET_KEY = "wYepiYriAlGLkejuZ55xBtTjMw^2k!yUK0wL0ifM6cXFX&A%vfT!23U1am3@Xzkm"

    # 数据库
    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:admin@localhost:3306/python_ihome"

    # 设置sqlalchemy自动跟踪数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Redis 配置
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_PASSWORD = "admin"

    # Session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    SESSION_USE_SIGNER = True  # 对Cookie_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 24 * 3600  # Session数据的有效期，单位：秒


class DevelopConfig(Config):
    """开发环境"""
    DEBUG = True


class ProductConfig(Config):
    """生产环境"""
    DEBUG = False


config_map = {
    "develop": DevelopConfig,
    "product": ProductConfig,
}
