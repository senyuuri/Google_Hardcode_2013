import urllib, urllib.request, urllib.parse, urllib.error

import re

def request(us, pw):
    #构建POST表单数据
    postdata=urllib.parse.urlencode({
        'username': us,
        'password': pw,
        'submit':'Connect >> '
    })
    
    #请求地址
    address = 'http://wireless.colubris.com:8080/goform/HtmlLoginRequest'

    #生成http请求并发送
    req = urllib.request.Request(address,postdata.encode('utf-8'))
    result = urllib.request.urlopen(req, timeout=10).read()

    #检查返回页面
    decoded_result=result.decode('utf-8')
    if re.search('LOADING', decoded_result): 
        return True
    else:
        return False

#用户名生成
default_username = "guest"
password = "hostel"
succ=False
t = 0
while(succ == False):
    for i in range (1,26):
        t+=1
        username = default_username
        username += str(i)
        print(username, ", count",t,)
        if request(username,password):
            print("Log in success!" )
            succ = True
            break
        else:
            print("Log in failed...")
