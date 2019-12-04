from core.crontab import Crontab
from core.crontab import Task
import __diy__

submiter = __diy__.submiter
submiter.start()

__diy__.preload()

attack_funcs = __diy__.attack_funcs
tasks = []
tasks.append(Task(__diy__.preload))
for funcs in attack_funcs:
    for ip in __diy__.TARGET_IPS:
        tasks.append(Task(funcs, args=(ip, )))

crontab = Crontab(tasks, 10)
crontab.start()
submiter.exit()
