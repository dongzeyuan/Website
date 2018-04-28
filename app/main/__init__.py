'''
这个模块用来定义蓝图：Blueprint
需要注意，views和errors在末尾导入
避免循环导入的问题
'''

from flask import Blueprint


main = Blueprint('main', __name__)

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

from . import views, errors
