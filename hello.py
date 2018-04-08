# encoding:utf-8

from flask import Flask, render_template

from flask_bootstrap import Bootstrap
import config

app = Flask(__name__)
app.config.from_object(config)

bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    app.run()
