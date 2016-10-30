# -*- coding: utf-8 -*-
# 引入Python SDK的包
import weibo
import base64
import rsa
import binascii
import requests
from weiboSpider import *
import cookielib
import json

#  只需要修改这里！！！
username = 'xxxx'   #登陆账号，邮箱或者手机号
password = 'xxxx'       #登陆密码


# 模拟授权登陆过程,getCode
#  http://blog.csdn.net/liujiandu101/article/details/52096654
# http://blog.csdn.net/zhanh1218/article/details/26383469

# 一个批量删除新浪微博发言的python脚本
# http://opengg.me/301/a-python-script-to-delete-weibo-tweets/s

def login():
    #username base64加密
    su = base64.encodestring(username)[:-1]

    # 对密码加密，需要servertime，nonce，pubkey，rsakv
    get_arg_url = 'https://login.sina.com.cn/sso/prelogin.php?' \
                  'entry=openapi&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&cl'%su
    get_arg = requests.get(get_arg_url)
    get_arg_content = get_arg.content
    get_arg_content_split = get_arg_content.split(',')
    servertime = get_arg_content_split[1].split(':')[1]
    nonce = get_arg_content_split[3].split(':')[1][1:-1]
    pubkey = get_arg_content_split[4].split(':')[1][1:-1]
    rsakv = get_arg_content_split[5].split(':')[1][1:-1]

    #password加密
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    sp = rsa.encrypt(message, key) #加密
    sp = binascii.b2a_hex(sp) #将加密信息转换为16进制。

    # 登录请求
    postPara = {
        'entry': 'openapi',
        'gateway': '1',
        'from': '',
        'savestate': '0',
        'userticket': '1',
        'pagerefer': '',
        'ct': '1800',
        's': '1',
        'vsnf': '1',
        'vsnval': '',
        'door': '',
        'appkey': '52laFx',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': sp,
        'sr': '1920*1080',
        'encoding': 'UTF-8',
        'cdult': '2',
        'domain': 'weibo.com',
        'prelt': '2140',
        'returntype': 'TEXT',
    }
    get_ticket_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    req = requests.post(get_ticket_url, postPara)
    #  add, 保存cookie

    cookies = req.cookies
    content = json.loads(req.content)
    uid = content['uid']

    # 保存cookie到cookie.txt中

    #ticket = req.content.split(',')[1].split(':')[1][1:-1]
    #print ticket

    # 实例化一个LWPcookiejar对象
    new_cookie_jar = cookielib.LWPCookieJar(username + '.txt')
    # 将转换成字典格式的RequestsCookieJar（这里我用字典推导手动转的）保存到LWPcookiejar中
    requests.utils.cookiejar_from_dict({c.name: c.value for c in cookies}, new_cookie_jar)
    # 保存到本地文件
    new_cookie_jar.save('cookies/' + uid + '.txt', ignore_discard=True, ignore_expires=True)
    print 'login successful， cookies saved'
    content = json.loads(req.content)
    print 'welcome, ' + content['nick']
    return uid

    '''
    fields = {
        'action': 'submit',  # 必须
        'display': 'default',
        'withOfficalFlag': '0',  # 必须
        'quick_auth': 'null',
        'withOfficalAccount': '',
        'scope': '',
        'ticket':ticket,  # 必须
        'isLoginSina': '',
        'response_type': 'code',  # 必须
        'regCallback': 'https://api.weibo.com/2/oauth2/authorize?client_id=' + APP_KEY + '\
                       &response_type=code&display=default&redirect_uri=' + CALL_BACK + '&from=&with_cookie=',
        'redirect_uri': CALL_BACK,  # 必须
        'client_id': APP_KEY,  # 必须
        'appkey62': 'kxR5R',
        'state': '',  # 必须
        'verifyToken': 'null',
        'from': '',  # 必须
        'userId': "",  # 此方法不需要填写明文ID
        'passwd': "",  # 此方法不需要填写明文密码
    }
    post_url = 'https://api.weibo.com/oauth2/authorize'
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ZHCNMSE; rv:11.0) like Gecko",
               "Referer":CALL_BACK,
               "Content-Type": "application/x-www-form-urlencoded",
               }

    get_code_url = requests.post(post_url, data=fields, headers=headers)
    url = get_code_url.url
    code = url[url.index('=')+1:]
    '''


'''
def Login():
    # weibo模块的APIClient是进行授权、API操作的类，先定义一个该类对象，传入参数为APP_KEY, APP_SECRET, CALL_BACK
    client = weibo.APIClient(APP_KEY, APP_SECRET, CALL_BACK)
    # 获取该应用（APP_KEY是唯一的）提供给用户进行授权的url
    auth_url = client.get_authorize_url()
    # 打印出用户进行授权的url，将该url拷贝到浏览器中，服务器将会返回一个url，该url中包含一个code字段（如图1所示）
    print "auth_url : " + auth_url
    # 输入该code值（如图2所示）

    code = getCode()
    print code
    #code = raw_input("input the retured code : ")
    # 通过该code获取access_token，r是返回的授权结果，具体参数参考官方文档：
    # http://open.weibo.com/wiki/Oauth2/access_token
    request = client.request_access_token(code)
    # 将access_token和expire_in设置到client对象
    client.set_access_token(request.access_token, request.expires_in)

    # 以上步骤就是授权的过程，现在的client就可以随意调用接口进行微博操作了，下面的代码就是用用户输入的内容发一条新微博
    return client
'''

def sendWeibo(client,content):
    if not content:
        content = raw_input('input the your new weibo content : ')

    # 调用接口发一条新微薄，status参数就是微博内容
    client.statuses.update.post(status=content)
    print "Send succesfully!"

def getWeibo(client):
    # 这个接口只能获取最近5条
    weibo = client.statuses.user_timeline.get()

    print weibo['statuses'][0]
    print "get succesfully!"






if __name__ == "__main__":
    uid = login()
    #sendWeibo(client,"三星牛逼")
    #getWeibo(client)
    ids = spider(int(uid))
    delWeibo(uid,ids)
