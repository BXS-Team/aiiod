import re


# ichunqiu AWD
def submit_flag_fn(**kw) -> bool:
    d = {
        'flag': kw['flag'],
        'token': TOKEN,
    }
    r = requests.post(SUBMIT_URL, data=d, verify=0)
    if 1:
        logger.success('ok: ' + kw['flag'])
        return True
    else:
        logger.error('err: ' + kw['flag'])
        return False


# 易霖博AWD提交flag处理验证码
# SUBMIT_URL = 'http://172.20.66.66/race.php/melee/sub_flag?scenes_id=6&id=13&module_id=4'
def submit_flag_fn(**kw) -> bool:
    url = SUBMIT_URL

    h = {
        'Cookie':
        'PHPSESSID=2l8nvnfg6vlu9dus1a8aoahrf0; _csrf=50ffc31f8e4712d305c020cc4a72b6899edcd5426bc946263357a4b6f2261bf0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ex2SiYb6kNoCQaaTVg32vJAw7YKlOB6h%22%3B%7D; token=434453743bef927d1a7389aba14aaaaf; __user_identity=d7d2962f0ab7e084906b22ee6dd2cb18f675ffcda146c9b0a96d2d458670b6aea%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22__user_identity%22%3Bi%3A1%3Bs%3A17%3A%22%5B15%2Cnull%2C2592000%5D%22%3B%7D'
    }

    s = requests.Session()
    s.headers.update(h)
    r = s.get(url, headers=h)
    _csrf = re.findall(
        r'\<meta name\="csrf-token" content\="([a-zA-Z0-9\=\/\+]+)"\>', r.text)
    _csrf = _csrf[0] if _csrf else ''
    if not _csrf:
        return False

    files = {
        '_csrf': (None, _csrf, None),
        'melee_ip': (None, kw['ip'].strip(), None),
        'melee_flag': (None, kw['flag'].strip(), None),
        'VerifyCode[file]': (None, '', None),
        'VerifyCode[verifyCode]': (None, 'SEPI', None),
        'btn-Submit': (None, '', None),
    }
    r = s.post(url, files=files, headers=h)
    msg = re.findall(r'\$\("\.message\-tishi"\)\.html\(\'(.+)\'\);', r.text)
    msg = msg[0] if msg else ''

    success = '恭喜您答对了' in msg
    if success:
        logger.success(f'attack {kw["ip"]} ok: {kw["flag"]} {msg}')
    else:
        logger.error(f'attack {kw["ip"]} fail: {kw["flag"]} {msg}')
    return success