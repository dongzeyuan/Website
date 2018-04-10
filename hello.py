# encoding:utf-8

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "index"

@app.route('/projects/')
def projects():
    return "projects page"

@app.route('/about')
def about():
    return "about page"





if __name__ == '__main__':
    app.run(debug=True)
