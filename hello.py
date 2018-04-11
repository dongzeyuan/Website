# encoding:utf-8

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    comments = ['你', '是', '大', '坏', '蛋']
    return render_template('index.html', comments=comments)


if __name__ == '__main__':
    app.run(debug=True)
