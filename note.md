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

打开浏览器，输入 `127.0.0.1:5000` 后会在页面显示 `Hello World！`