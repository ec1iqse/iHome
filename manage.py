# -*- coding:utf-8 -*-
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager

from iHome import create_app
from iHome import db

# 创建Flask应用对象
app = create_app(mode="develop")

manager = Manager(app=app)
Migrate(app=app, db=db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
