# encoding:utf-8

from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def index():
    return '<h1>config 配置!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run()
