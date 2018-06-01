#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import re
import urllib
import urllib2
# 得这样导入
from bs4 import BeautifulSoup

# 抓取淘女郎
# 如果网页找不到，就是ajax异步加载，去xhr里去找
# 右键看源码
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
# 注意：form data请求参数
params = 'q&viewFlag=A&sortType=default&searchStyle=&searchRegion=city%3A&searchFansNum=&currentPage=1&pageSize=100'


def getHome():
    url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
    req = urllib2.Request(url, headers=headers)
    # decode（’utf - 8’）解码   把其他编码转换成unicode编码
    # encode(’gbk’) 编码  把unicode编码转换成其他编码
    # ”gbk”.decode(’gbk’).encode(’utf - 8')
    # unicode = 中文
    # gbk = 英文
    # utf - 8 = 日文
    # 英文一 > 中文一 > 日文,unicode相当于转化器
    html = urllib2.urlopen(req, data=params).read().decode('gbk').encode('utf-8')
    # json转对象
    peoples = json.loads(html)
    for i in peoples['data']['searchDOList']:
        getUseInfo(i['userId'], i['realName'])
        # print i


def getUseInfo(userId, realName):
    url = 'https://mm.taobao.com/self/aiShow.htm?userId=' + str(userId)
    req = urllib2.Request(url)
    html = urllib2.urlopen(req).read().decode('gbk').encode('utf-8')

    pattern = re.compile('<img.*?src=(.*?)/>', re.S)
    items = re.findall(pattern, html)
    x = 0
    for item in items:
        if re.match(r'.*(.jpg")$', item.strip()):
            tt = 'http:' + re.split('"', item.strip())[1]
            # print tt
            down_image(tt, x, realName)
            x = x + 1
    print('下载完毕')


def down_image(url, filename, realName):
    req = urllib2.Request(url=url)
    folder = 'e:\\images\\%s' % realName
    if os.path.isdir(folder):
        pass
    else:
        os.makedirs(folder)

    f = folder + '\\%s.jpg' % filename
    if not os.path.isfile(f):
        print f
        binary_data = urllib2.urlopen(req).read()
        with open(f, 'wb') as temp_file:
            temp_file.write(binary_data)


getHome()
