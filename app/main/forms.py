'''
定义表单类
目前只有一个表单，NameForm表单
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

# 定义NameForm表单类，基于FlaskForm类生成
class NameForm(FlaskForm):
    # name是个文本字段，validators添加一个验证函数组成的列表，
    # Required验证函数确保字段中有数据
    name = StringField('What is your name?', validators=[Required()])
    # 添加一个表单提交按钮，按钮名字为Submit
    submit = SubmitField('Submit')
