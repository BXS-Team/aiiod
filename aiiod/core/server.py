from flask import Flask, request
import threading


def start_callback_server(add_flag_fn, callback=None, port=80):
    app = Flask(__name__)

    def default_callback():
        flag = request.form['flag']
        ip = request.remote_addr
        print('[+]server recv from ' + ip + ': ' + flag)

        if len(flag) > 0 and len(flag) < 50:
            add_flag_fn({'flag': flag, 'ip': ip})
        return ''

    app.add_url_rule(
        '/', 'index', callback or default_callback, methods=('POST', ))

    threading.Thread(target=app.run, args=('0.0.0.0', port)).start()