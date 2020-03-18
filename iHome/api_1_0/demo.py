# -*- coding:utf-8 -*-
from flask import current_app
from iHome import models
from iHome import db
from . import api


@api.route(rule="/index", methods=["GET", "POST"])
def index():
    current_app.logger.error("error message")
    current_app.logger.warn("warn message")
    current_app.logger.info("info message")
    current_app.logger.debug("debug message")
    return "Hello World!"
