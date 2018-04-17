# 安装
## 安装flask
1. 创建虚拟环境：
* 启动cmd，切记之后所有的操作都是在cmd中执行，不是在powershell中执行
* 切换到想要创建虚拟环境文件夹的目录，例如C:\Python36
* 执行如下命令
    cmd
    mkdir python-env
    cd python-env
    python -m venv flask-env
2. 在vs code中使用虚拟环境
3. 机械硬盘眼看要挂，直接换了ubuntu，现在在升级
4. 在Ubuntu上折腾了怎么安装软件，解决了图标问题，很厉害

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

试验一下ssh是不是成功了






