# encoding:utf-8

from flask import Flask
from flask import redirect
app = Flask(__name__)


@app.route('/')
def index():
    # 重定向
    return redirect('https://www.baidu.com')

@app.route('/projects/')
def projects():
    return "projects page"

@app.route('/about')
def about():
    return "about page"





if __name__ == '__main__':
    app.run(debug=True)
