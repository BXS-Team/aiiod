import datetime
import sys
# from colorama import Fore

now = lambda: datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')

log_file = open('./log.txt', 'a+', buffering=1)

_output = [sys.stdout, log_file]


def log(msg):
    [dst.writelines(f'[+] {now()} {msg}\n') for dst in _output]


def success(msg):
    [dst.writelines(f'[*] {now()} {msg}\n') for dst in _output]


def error(msg):
    [dst.writelines(f'[!] {now()} {msg}\n') for dst in _output]