#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2

response = urllib2.urlopen("http://www.baidu.com")
# print response.read()

# 推荐这么写
values = {"username": "1016903103@qq.com", "password": "XXXX"}
# values = {}
# values['username'] = "1016903103@qq.com"
# values['password'] = "XXXX"
data = urllib.urlencode(values)

# post
# url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
# request = urllib2.Request(url, data)

# get
# url = "http://passport.csdn.net/account/login"
# geturl = url + "?" + data
# request = urllib2.Request(geturl)
# print geturl


# 添加head
url = 'http://www.server.com/login'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

values = {'username': 'cqc', 'password': 'XXXX'}
# headers = {'User-Agent': user_agent}
# head加入Referer应付盗链
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
           'Referer': 'http://www.zhihu.com/articles'}

request = urllib2.Request(url, data, headers)

response = urllib2.urlopen(url, timeout=10)
print response.read()

# Proxy（代理）的设置
enable_proxy = True
proxy_handler = urllib2.ProxyHandler({"http": 'http://some-proxy.com:8080'})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)

# put/delete请求
request = urllib2.Request(url, data=data)
request.get_method = lambda: 'PUT'  # or 'DELETE'
response = urllib2.urlopen(request)

# 使用 DebugLog
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.baidu.com')

# 异常捕获
req = urllib2.Request('http://blog.csdn.net/cqcre')
try:
    urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.code
except urllib2.URLError, e:
    if hasattr(e, "reason"):
        print e.reason
else:
    print "OK"
