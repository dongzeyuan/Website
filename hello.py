# encoding:utf-8

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/projects/')
def projects():
    return "projects page"


@app.route('/about')
def about():
    return "about page"


if __name__ == '__main__':
    app.run(debug=True)
