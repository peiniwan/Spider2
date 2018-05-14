#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Meizi:
    def __init__(self):
        self.pageIndex = 1
        # 反链
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化 headers
        self.headers = {'User-Agent': self.user_agent}

        # self.headers = {'Referer': 'http://www.mzitu.com/134368'}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    def getPage(self):
        url = 'http://www.mzitu.com/134368'
        req = urllib2.Request(url, headers=self.headers)
        html = urllib2.urlopen(req).read()
        # html = html.decode("utf-8")
        print html
        pattern = re.compile('<div class="main-image">.*?<img src="(.*?)".*?/>', re.S)
        # pattern = re.compile('<h2 class="main-title">(.*?)</h2>', re.S)
        # pattern = re.compile('<link rel="canonical" href="(.*?)" />', re.S)

        pic = re.findall(pattern, html)
        print pic

    def start(self):
        self.getPage()


meizi = Meizi()
meizi.start()
