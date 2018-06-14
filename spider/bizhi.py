# -*- coding: utf-8 -*-


import os
from threading import Thread

import requests
import time
import random
from lxml import etree

# 爬取wallhaven上的的图片，支持自定义搜索关键词，自动爬取并该关键词下所有图片并存入本地电脑。
# 练习多线程，ip代理

keyWord = raw_input(u"{'Please input the keywords that you want to download :'}")


class Spider():
    # 初始化参数
    def __init__(self):
        # headers是请求头，"User-Agent"、"Accept"等字段都是通过谷歌Chrome浏览器查找的！
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
        }
        self.proxies = {  # 代理ip，当网站限制ip访问时，需要切换访问ip
            "http": "http://61.178.238.122:63000",
        }
        # filePath是自定义的，本次程序运行后创建的文件夹路径，存放各种需要下载的对象。
        self.filePath = ('d:/python桌面壁纸/' + keyWord + '/')

    def creat_File(self):
        # 新建本地的文件夹路径，用于存储网页、图片等数据！
        filePath = self.filePath
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    def get_pageNum(self):
        # 用来获取搜索关键词得到的结果总页面数,用totalPagenum记录。由于数字是夹在形如：1,985 Wallpapers found for “dog”的string中，
        # 所以需要用个小函数，提取字符串中的数字保存到列表numlist中，再逐个拼接成完整数字。。。
        total = ""
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc").format(
            keyWord)
        html = requests.get(url)
        selector = etree.HTML(html.text)
        pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')
        string = str(pageInfo[0])
        numlist = list(filter(str.isdigit, string))
        for item in numlist:
            total += item
        totalPagenum = int(total)
        return totalPagenum

    def main_fuction_1(self):
        # count是总图片数，times是总页面数
        self.creat_File()
        count = self.get_pageNum()
        print("We have found:{} images!".format(count))
        times = int(count / 24 + 1)
        j = 1
        start = time.time()
        for i in range(times):
            pic_Urls = self.getLinks(i + 1)
            start2 = time.time()
            for item in pic_Urls:
                self.download(item, j)
                j += 1
            end2 = time.time()
            print('This page cost：', end2 - start2, 's')
        end = time.time()
        print('Total cost:', end - start, 's')

    def main_fuction_2(self):
        # count是总图片数，times是总页面数
        self.creat_File()
        count = self.get_pageNum()
        print("We have found:{} images!".format(count))
        times = int(count / 24 + 1)
        j = 1
        start = time.time()
        for i in range(times):
            pic_Urls = self.getLinks(i + 1)
            start2 = time.time()
            threads = []
            for item in pic_Urls:
                t = Thread(target=self.download, args=[item, j])
                t.start()
                threads.append(t)
                j += 1
            for t in threads:
                t.join()
            end2 = time.time()
            print('This page cost：', end2 - start2, 's')
        end = time.time()
        print('Total cost:', end - start, 's')

    def getLinks(self, number):
        # 此函数可以获取给定numvber的页面中所有图片的链接，用List形式返回
        url = (
            "https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc&page={}").format(
            keyWord, number)
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            pic_Linklist = selector.xpath('//a[@class="jsAnchor thumb-tags-toggle tagged"]/@href')
        except Exception as e:
            print(repr(e))
        return pic_Linklist

    def download(self, url, count):
        # 此函数用于图片下载。其中参数url是形如：https://alpha.wallhaven.cc/wallpaper/616442/thumbTags的网址
        # 616442是图片编号，我们需要用strip()得到此编号，然后构造html，html是图片的最终直接下载网址。
        string = url.strip('/thumbTags').strip('https://alpha.wallhaven.cc/wallpaper/')
        html = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string + '.jpg'
        pic_path = (self.filePath + keyWord + str(count) + '.jpg')
        try:
            pic = requests.get(html, headers=self.headers)
            f = open(pic_path, 'wb')
            f.write(pic.content)
            f.close()
            print("Image:{} has been downloaded!".format(count))
            time.sleep(random.uniform(0, 2))  # 为了防止反爬
        except Exception as e:
            print(repr(e))


spider = Spider()
# spider.main_fuction_1()
spider.main_fuction_2()  # 多线程
