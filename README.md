# aiiod

AWD Framework written by BXS Team

### Project

```
aiiod
|  aiiod.py               # 入口文件，启动定时任务
|  __diy__.py             # 自定义编码，需自定义攻击、提交flag、初始化等功能
|
|__core
|  |  crontab.py          # 定时任务模块
|  |  exceptions.py
|  |  globals.py
|  |  logger.py
|  |  server.py           # flag回调接收服务
|  |  submit.py           # flag提交模块，单例 + 单线程 + Prod/Cons模型
|  |  utils.py
|  |  __init__.py
|  |__connector           # 内置连接类
|       | database.py     # 实现MySQL, MSSQL连接、查询
|       | shell.py        # 实现Linux/Windows交互式R/W流量转发
|       | ssh.py          # 实现ssh command/interactive/upload/download
|       | bindtcpshell.py # 实现连接正向bind_shell command/interactive
|       |_webshell.py     # 实现PHP/ASPX/JSP等WebShell命令执行
|                         #     和PHP WebShell文件上传、PHP冰蝎马命令执行   
|
|_misc
|   | persistence.py      # 持久化模块
|   |_shittt.py           # 搅屎模块
|
|_scripts                 # 内置脚本
    | file-protect.py
    | log.php
    |_logwithdefend.php
```

### Usage

在`__diy__.py`中编写攻击和提交flag代码，从`aiiod.py`启动

```
$ python3 aiiod.py
```

### QA

+ Reverse shell需通过更稳定的持久化管理器接收
+ `__diy__.py`中的攻击函数需以`_a_`开头以被自动加载
+ 仅支持Python3.6+，系统不限

### [Contributors](https://github.com/BXS-Team/aiiod/graphs/contributors)