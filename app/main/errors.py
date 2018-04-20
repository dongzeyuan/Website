from flask import render_template
# 导入蓝图（注意蓝图模块中也导入了errors文件）
from . import main

# 使用蓝图定义错误路由
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# 使用蓝图定义错误路由
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500