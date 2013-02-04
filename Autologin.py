import urllib, urllib2, urllib.request, urllib.parse, urllib.error

import re

#用户名生成
username = "guest"
password = "hostel"

#创建表单数据
postdata=urllib.urlencode({
    'username': username,
    'password': password,
    'submit':'Connect >> '
})

address = 'http://wireless.colubris.com:8080/goform/HtmlLoginRequest'
#生成http请求并发送
req = urllib2.request(address,postdata)
result = urllib2.urlopen(req).read()

#检查返回页面
decoded_result=result.decode('utf-8')

if re.search('{} HOME'.format(USER), decoded_result): 
    print("Log in success!" )
else:
    with open('result.html','w') as f:
        f.write(result)
    print("Log in failed...")

input()
