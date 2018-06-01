# -*- coding: utf-8 -*-
import cookielib
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

response = urllib2.urlopen(url, timeout=5)
print response.read()

# Proxy（代理）的设置, 代理IP地址，防止自己的IP被封禁
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


# 可以利用 cookie 实现模拟登录
# 利用 CookieJar 对象实现获取 cookie 的功能，存储到变量中
# 声明一个 CookieJar 对象实例来保存 cookie
cookie = cookielib.CookieJar()
# 利用 urllib2 库的 HTTPCookieProcessor 对象来创建 cookie 处理器
handler = urllib2.HTTPCookieProcessor(cookie)
# 通过 handler 来构建 opener
opener = urllib2.build_opener(handler)
# 此处的 open 方法同 urllib2 的 urlopen 方法，也可以传入 request
response = opener.open('http://www.baidu.com')
for item in cookie:
    print 'Name =' + item.name
    print 'Value =' + item.value

# 保存
# 设置保存 cookie 的文件，同级目录下的 cookie.txt
filename = 'cookie.txt'
# 声明一个 MozillaCookieJar 对象实例来保存 cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
# 利用 urllib2 库的 HTTPCookieProcessor 对象来创建 cookie 处理器
handler = urllib2.HTTPCookieProcessor(cookie)
# 通过 handler 来构建 opener
opener = urllib2.build_opener(handler)
# 创建一个请求，原理同 urllib2 的 urlopen
response = opener.open("http://www.baidu.com")
# 保存 cookie 到文件
# ignore_discard：cookies 将被丢弃也将它保存下来
# ignore_expires：如果在该文件中 cookies 已经存在，则覆盖原文件写入
cookie.save(ignore_discard=True, ignore_expires=True)

# 创建 MozillaCookieJar 实例对象
cookie = cookielib.MozillaCookieJar()
# 从文件中读取 cookie 内容到变量
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# 创建请求的 request
req = urllib2.Request("http://www.baidu.com")
# 利用 urllib2 的 build_opener 方法创建一个 opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
print response.read()
# 如果cookie.txt 文件中保存的是某个人登录百度的 cookie，
# 那么提取出这个 cookie 文件内容，就可以用以上方法模拟这个人的账号登录百度


