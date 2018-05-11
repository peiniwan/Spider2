#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cookielib
import urllib
import urllib2

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


# 利用 cookie 实现模拟登录，并将 cookie 信息保存到文本文件中
filename = 'cookie.txt'
# 声明一个 MozillaCookieJar 对象实例来保存 cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
    'stuid': '201200131012',
    'pwd': '23342321'
})
# 登录教务系统的 URL
loginUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
# 模拟登录，并把 cookie 保存到变量
result = opener.open(loginUrl, postdata)
# 保存 cookie 到 cookie.txt 中
cookie.save(ignore_discard=True, ignore_expires=True)
# 利用 cookie 请求访问另一个网址，此网址是成绩查询网址
gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
# 请求访问成绩查询网址
result = opener.open(gradeUrl)
print result.read()
