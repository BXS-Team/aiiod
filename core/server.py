from flask import Flask, request

from core.submit import Submiter

s = Submiter()

app = Flask(__name__)


@app('/', methods=['POST'])
def index():
    flag = request.form['flag']
    print('server recv: ' + flag)
    s.add_flag(flag=flag)


app.run('0.0.0.0', 5000)