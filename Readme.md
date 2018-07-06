<!-- TOC -->

- [疑难杂症](#疑难杂症)
    - [github 不显示 contribution](#github-不显示-contribution)
    - [创建数据库迁移脚本](#创建数据库迁移脚本)
    - [VSCode快捷键](#vscode快捷键)
- [Flask 笔记](#flask-笔记)
    - [安装Flask虚拟环境](#安装flask虚拟环境)
        - [windows下](#windows下)
    - [flask程序的基本结构](#flask程序的基本结构)
        - [请求调度](#请求调度)
    - [数据库](#数据库)
        - [Flask-SQLAlchemy](#flask-sqlalchemy)
        - [定义模型](#定义模型)
        - [关系](#关系)
        - [在python shell里进行数据库操作](#在python-shell里进行数据库操作)
        - [在视图函数中操作数据库](#在视图函数中操作数据库)
    - [大型项目的构架](#大型项目的构架)
        - [项目结构](#项目结构)
        - [我对项目构架的理解](#我对项目构架的理解)

<!-- /TOC -->

# 疑难杂症

## github 不显示 contribution
点开不显示contribution的commit，在网页后加.patch

查看邮箱是否和该github账户邮箱一样，如果不同，是不会显示contribution

打开终端，输入以下命令：

```bash
git config --global "xxxxx@xx.com"
```

## 创建数据库迁移脚本
```shell
cd 至项目根目录（manage.py所在那一层目录）

# 其中migrate tag是指自定义的标记，类似git的commit内容
# 这样就生成了迁移脚本
(venv) $ python manage.py db migrate -m "migrate tag"

# 执行升级脚本upgrade命令，升级到最新数据库
(venv) $ python manage.py db upgrade
```

## VSCode快捷键
```
折叠代码：CTRL+K   CTRL+0
展开代码：CTRL+K   CTRL+J
```

# Flask 笔记
## 安装Flask虚拟环境
### windows下
必须使用cmd命令行

    mkdir pyenv                 #在当前目录创建pyenv文件夹，用来保存Python的虚拟环境
    cd pyenv                    #切换到pyenv文件夹
    python -m venv flask        #python3使用内置的pyenv库创建flask虚拟环境（是个文件夹）
    cd flask                    #切换到flask虚拟环境文件夹中
    cd scripts                  #切换到scripts文件夹中
    activate.bat                #运行scripts中的activate.bat文件，开启虚拟环境

在vscode中配置工作区的虚拟环境：进入工作区的.settings.json文件，修改下列配置：
    
    python.pythonPath: 修改为虚拟环境下的python.exe路径
    python.venvPath: 修改为虚拟环境下的python.exe路径

使用虚拟环境的好处是在虚拟环境下安装的库只会安装到虚拟环境文件夹中，python的母体不会有任何改变，同时能方便的生成虚拟环境配置文件，列出虚拟环境中安装的库的名称和版本，在部署服务器是能方便的用命令调用配置文件自动安装所需的库。

## flask程序的基本结构

一个最基本的程序结构如下：

```python
# 引入Flask对象
from flask import Flask

# 实例化一个app，传参是__name__
app = Flask(__name__)


# @app.route定义一个路由
@app.route('/')
# 定义视图函数 index()
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

打开浏览器，输入 `127.0.0.1:5000` 后会在页面显示 `Hello World！`

### 请求调度

在路由中，一般会默认指定视图函数返回的url地址，如果需要反过来，只知道视图函数，然后调用对应的url，可以使用`url_for()`函数

## 数据库

* 关系型数据库——SQL数据库
* 文档数据库和键值对数据库——NoSQL数据库

SQL数据库把数据存储在 `表` 中，各个表对应程序中不同的实体。
    
    order.data
    |——customers
    |——products
    |——orders

表的 `列` 数是固定的，`行` 数是可变的。
* 列——表的实体的数据属性

customers表中的列名称：

    customers：
    name    address     phone

* 行——列对应的真实数据值
* 主键，外键

### Flask-SQLAlchemy

使用Flask-SQLAlchemy配置SQLite数据库的示例：

```python
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 下面那个URI确实是I不是L
# data.sqlite是配置的数据库的名称
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# db对象是SQLAlchemy的实例
db = SQLAlchemy(app)
```

### 定义模型

`模型` 表示程序使用的持久化实例，模型一般是一个python的类，类中的属性对应数据库`表`中的`列`。

Flask-SQLAlchemy创建的数据库实例为模型提供了一个基类以及一系列辅助类和辅助函数，可以用于定义模型的结构。

定义Role和User模型：

```python
# 基类是 db.Model
class Role(db.Model):

    # 定义数据库中的表名，如果不定义__tablename__，Flask-SQLAlchemy
    # 会生成默认的表名，但是默认的表名不遵守使用复数形式进行命名的约定（滑稽脸）
    __tablename__ = 'roles'

    # 主键（primary_key=True)，定义成db.Column类的实例
    id = db.Column(db.Interger, primary_key=True)

    # name，定义成db.Column类的实例
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Interger, primary_key=True)

    # unique和index都是属性配置选项，unqiue=True表示列不允许出现重复值
    # index=True表示为此列建立索引，提高查询效率
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.userna‵‵
```

### 关系

关系型数据库使用关系把不同`表`中的`行`联系起来。例如上面的Role模型和User模型，一个role（角色）可以对应多个user（用户），但是一个user只能有一个role。

这种一对多关系，在模型类中的表示方法如下：
```python
class Role(db.Model):
    # ...

    # 这里用db.relationship方法构建关系,
    # 其实是在User类中新增了 role 列属性
    users = db.relationship('User',backref='role')

class User(db.Model):
    # ...

    # 下面实际上是在User类中创建了role的新列
    # 在User的新列里添加了新列 role_id,并定义其为外键
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
```

在一对多关系中，只能对应一个的那个类使用添加列的方式增加列属性；能对应多个的那个类使用db.relationship添加关系

### 在python shell里进行数据库操作

1. 创建表

    使用db.creat_all()函数创建数据库

```python
(venv) python shell

>>>from hello import db
>>>db.creat_all()
```
如果数据库的表（hello.py文件中定义的两个表）已经存在于数据库中，那么db.creat_all()不会重新创建或者更新这两个表的。

2. 插入行

```python
>>>from hello import Role, User
>>>admin_role = Role(name='Admin')
>>>mod_role = Role(name='Moderator')
>>>user_role = Role(name='User')
>>>user_john = User(username='john',role=admin_role)
>>>user_susan = User(username='susan',role=user_role)
>>>user_david = User(username='david',role=user_role)
```
上面其实并没有将数据写入库中，在写入数据库前，先将其添加到对话中

```python
>>>db.session.add(admin_role)
或者
>>>db.session.add_all([admin_role,mod_role,user_role,user_john,user_susan,user_david])
```
最后使用commit()方法提交会话

```python
>>>db.session.commit()
```
可以看出，在pythonshell中添加数据比较麻烦，

创建-----添加到会话中（db.session.add 或者db.session.add_all)------db.session.commit()


3. 修改行
```
db.session.add()
```
4. 删除行
```
db.session.delete()
```
5. 查询行
```
Role.query.all()
User.query.filter_by(role=user_role).all()
```
`filter_by()` 是查询过滤器，还有不同的查询过滤器，这里不在叙述

`all()`是查询执行函数

### 在视图函数中操作数据库

```python
@app.route('/',methods=['GET','POST'])
def index():

    # 生成表单类实例
    form = NameForm()

    # validate_on_submit()函数用于验证表单是否收到用户的输入
    # 如果用户输入有效值，该方法返回True，否则返回False
    if form.validate_on_submit():

        # 使用query对象的filter_by()过滤器查询输入的表单值是否在数据库内，如果在数据库内，user不为None，否则返回None
        user = User.query.filter_by(username=form.name.data).first()

        # 如果输入的表单值不在数据库内
        if user is None:

            # 将输入的表单值赋值给User类的username列，然后将名字赋值给user变量
            user = User(username = form.name.data)

            # 数据库会话中增加 user（表单输入值）
            db.session.add(user)

            # 请求上下文中的known变量设定为Fasle（这个人在数据库中没有）
            session['known'] = False

        # 如果输入的表单值在数据库内
        else:

            # 请求上下文的known变量设定为True（这个人在数据库中）
            session['known'] = True

        # 将输入的表单值赋值给请求上下文的 name 变量
        session['name'] = form.name.data

        # 将输入的表单值设定为空
        form.name.data = ''

        # 重定向，返回inex视图函数的url
        return redirect(url_for('index'))

    # 返回渲染模板中的index.html文件，同时给模板中的占位变量赋值
    return render_template('index.html',form = form,
                            name = session.get('name'),
                            known = session.get('known',False))
```

对应的模板

```html
{% block page_content %}
<div class="page-header">
    <h1>Hello, {% if name %} {{ name }}{% else %}Stranger{% endif %}!</h1>
    <!-- 下面是模板中根据程序中的known取值不同显示不同的欢迎信息-->
    {% if not known %}
    <p>Pleased to meet you!</p>
    {% if known %}
    <p>Happy to see you again</p>
    {% endif %}
</div>
```

在这个视图函数中，提交表单后，程序使用filter_by()过滤器在数据库中查询提交的名字。变量known被写入用户会话中，因此在重定向后可以把数据传给模板，用来显示自定义的欢迎信息。

## 大型项目的构架

### 项目结构
Flask程序的基本结构如下：


```
D:.
|   config.py                           生成配置文件
|   data-dev.sqlite                     项目数据库文件
|   manage.py                           项目启动文件
|   note.md 
|   requirements.txt                    项目运行环境描述
+---app                                 /程序包文件夹
|   |   email.py                        邮件脚本
|   |   models.py                       数据模型
|   |   __init__.py                     工厂函数&注册蓝本
|   |
|   +---auth                            /用户认证模块
|   |   |   forms.py                    用户认证表单文件
|   |   |   views.py                    用户认证视图函数
|   |   |   __init__.py                 用户认证蓝图
|   |   |
|   |
|   +---main                            /主程序
|   |   |   errors.py                   错误信息
|   |   |   forms.py                    主程序表单文件
|   |   |   views.py                    主程序视图函数
|   |   |   __init__.py                 主程序蓝图
|   |   |
|   |
|   +---static                          /app下的静态文件包
|   |       favicon.ico                 网站缩略图标
|   |
|   +---templates                       /模板文件
|   |   |   404.html                    
|   |   |   500.html
|   |   |   base.html
|   |   |   index.html
|   |   |   user.html
|   |   |
|   |   \---auth                        /用户认证模块的模板文件
|   |           login.html
|   |           register.html
|   |
|
+---migrations
|   |   alembic.ini
|   |   env.py
|   |   README
|   |   script.py.mako
|   |
|   +---versions
|
+---tests
|       test.py
|       test_user_model.py
|       __init__.py
|
```

```
上面那个文件夹结构，使用tree命令生成
tree 生成当前目录的结构图，默认只输出文件夹
tree /f 生成当前目录结构图，包括文件夹内文件
tree /a 换另一种样式
上面的结构命令是： tree /f /a
```
共计4个顶级文件夹：
* app 包中存放Flask程序
* migrations 存放数据库迁移文件
* test 存放单元测试脚本
* venv 包含python虚拟环境

同时还创建了一些文件

* requirements.txt 列出了所有的依赖包，便于在其他文件中重新生成相同的虚拟环境
* config.py 存储配置文件
* manage.py 用于启动程序以及其他的程序任务

### 我对项目构架的理解

1. 首先app文件夹中的`./app/__init__.py`文件引入程序的库，生成工厂函数。所谓的工厂函数，就是定义一个外部函数，这个函数简单的生成并返回一个内嵌的函数，仅仅是返回但是不调用，通过调用这个工厂函数，可以得到内嵌函数的一个引用，内嵌函数就是通过调用工厂函数时运行内部的def语句而创建的。例如：

```python
# 工厂函数 maker
def maker(n):
    k = 8

    # 内嵌函数 action
    def action(x):
        return x**n+k
    return action
```

在flask中，具体的工厂函数例子如：

```python
def create_app(config_name):

    #生成Flask实例，app
    app = Flask(__name__)
    # 通过flask的config.from_object()方法引入外部配置
    # 这里一定要注意，传递的参数时config文件中的config字典中的key
    # 所以携程config[config_name]的形式
    app.config.from_object(config[config_name])

    # config包中的config字典中对应的开发环境基类中的.init_app()方法
    # 这个地方比较绕
    # config文件中定义了class Config，内含一个.init_app()的静态方法
    # config文件中其他所有的类都继承自Config类，所以也都继承了.init_app()方法
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 返回app实例
    return app

```

2. 项目文件夹 `./config` 配置程序，建立了基本的配置，生成了几种工作环境的设置：
    * developmentconfig
    * testingconfig
    * productionconfig
    * defaultconfig（默认设置为开发环境）
3. 程序的蓝本，在`./app/main/__init__.py`文件中创建蓝本，蓝本程序形如：
```python
from flask import Blueprint

# 生成蓝本实例
# 蓝本程序一般接受两个参数，第一个是蓝本的名字，
# 第二个是蓝本所在的包或模块
main = Blueprint('main',__name__)

# 这里的两个模块需要在 __init__.py脚本的末尾导入，
# 这是为了避免循环导入依赖，在views和errors中还要导入蓝本main
from . import views, errors
```
在__init__.py
今天太忙了，水一发
水一发，删了DOTA，这游戏毁人不倦

这一个半月荒废了
到底该用python做点什么好？
学完没用，或者是自己技艺不精导致无法使用
很悲伤


今天打了50份文件，年轻人，到底是靠不住


主播艺伎化

这段时间荒废了很多，dota2太好玩了

今天买了新键盘，单位的事情也办的差不多了，是时候开启一波学习的浪潮了

发现了新体系？

去医院挂急诊拍了个片，幸好无大碍

和儿子严肃的商量了一下用小猪佩奇厨房套装玩具换回他的IKBC C87键盘

儿子急性阑尾炎，周六下午七点半拉完粑粑开始肚子疼，开始没太注意，看我儿子一头汗脸色苍白，到十点半又开始疼
感觉不对劲儿，赶紧去急诊，彩超看完发现阑尾肿大。已经住院两天了，愿我儿子早点康复。

儿子昨晚九点多开始退烧，今天情况大好。


我看他是彻底好了！闹得跟个泥猴一样！

买的厨房套装到了。。。。玩了一晚上
打算明天中午做鸡丝面，买的鸡胸肉煮的有点过了，没嚼劲，不过正好不塞儿子牙缝。

好多事儿！唉！