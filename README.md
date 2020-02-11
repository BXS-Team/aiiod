# aiiod

AWD Framework written by BXS Team

### Project

```
aiiod
|
|__core
|  |  crontab.py          # 定时任务模块
|  |  exceptions.py
|  |  globals.py
|  |  logger.py
|  |  server.py           # flag回调接收服务
|  |  submit.py           # flag提交模块，单例 + 单线程 + Prod/Cons模型
|  |  utils.py
|  |  target.py
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
|   | obscure.py          # 混淆流量
|   | persistence.py      # 持久化模块
|   |_shittt.py           # 搅屎模块
|
|_scripts                 # 内置脚本
    | file-protect.py
    | log.php
    |_logwithdefend.php
```

### Usage

See `run.py`

### [Contributors](https://github.com/BXS-Team/aiiod/graphs/contributors)