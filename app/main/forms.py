'''
定义表单类
目前只有一个表单，NameForm表单
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms import ValidationError
from wtforms.validators import Required, Length, Regexp, Email

# 定义NameForm表单类，基于FlaskForm类生成


class NameForm(FlaskForm):
    # name是个文本字段，validators添加一个验证函数组成的列表，
    # Required验证函数确保字段中有数据
    name = StringField('What is your name?', validators=[Required()])
    # 添加一个表单提交按钮，按钮名字为Submit
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    sumbit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[
                        Required(), Length(1, 64), Email()])
    username = StringField('Username0', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters,'
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(self, *args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
