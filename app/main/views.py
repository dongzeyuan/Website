from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from ..decorators import admin_required


# 导入蓝图函数
from . import main
# 从表单定义文件中引入表单类
from .forms import NameForm, EditProfileForm, PostForm
# 从./app/__init__.py中引入db
from .. import db
# 从模型类引入User模型
from ..models import User, Role, Permission, Post

# 蓝图中定义的程序路由


@main.route('/', methods=['GET', 'POST'])
def index():
    ''' # 实例化表单类,记得实例化时类名加括号
    # 写成 form = NameForm下面会报错
    form = NameForm()
    # 表单有数据提交:
    if form.validate_on_submit():
        # 对User数据库表进行查询，查询form.name.data的值是否在username列中
        user = User.query.filter_by(username=form.name.data).first()
        # 用户名不在数据库中：
        if user is None:
            # 将form.name.data赋值给User数据库表的username列
            user = User(username=form.name.data)
            # 数据库回话中添加输入的用户名
            db.session.add(user)
            # 程序上下文中 Known值设定为假
            session['known'] = False
            # 发送邮件
            if current_app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        # 如果用户名在数据库中
        else:
            # 程序上下文中known值设定为真
            session['known'] = True
        # 程序上下文中的name设定为用户名
        session['name'] = form.name.data
        # 清空用户名
        form.name.data = ''
        # 返回重定向的URL
        return redirect(url_for('index'))
    # 返回模板，给模板中的占位符赋值
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())'''

    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.send_email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.email.data = user.send_email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
