# -*- coding: utf-8 -*-
# !/usr/bin/env python
import random
import re

import pymysql
import requests
from bs4 import BeautifulSoup
import os


# 抓妹子图，并保存到数据库
class mzitu():

    def all_url(self, url):
        html = self.request(url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for index, a in enumerate(all_a):
            title = a.get_text()
            if (cmp(title, u'早期图片') == 0):
                continue
            href = a['href']
            lists = self.html(href, title)
            for i in lists:
                # print(i['meiziid'], i['title'], i['picname'], i['page_url'], i['img_url'])
                # 插入数据到数据库sql语句，%s用作字符串占位
                sql = "INSERT INTO `meizi_meizis`(`mid`,`title`,`picname`,`page_url`,`img_url`) VALUES(%s,%s,%s,%s,%s)"
                # try:
                cursor.execute(sql, (i['meiziid'], i['title'], i['picname'], i['page_url'], i['img_url']))
                db.commit()
                print(i['meiziid'] + " is success")
                # except:
                #     print(i['meiziid'] + " is fail")
                #     db.rollback()
        db.close()  # 关闭数据库

    def html(self, href, title):
        lists = []
        meiziid = href.split('/')[-1]
        html = self.request(href)
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            meizi = {}
            page_url = href + '/' + str(page)
            img_html = self.request(page_url)
            img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
            picname = img_url[-9:-4]
            # img = self.requestpic(img_url, page_url)
            meizi['meiziid'] = meiziid
            meizi['title'] = title
            meizi['picname'] = picname
            meizi['page_url'] = page_url
            meizi['img_url'] = img_url
            lists.append(meizi)  # 保存到返回数组中
        return lists

    def createAndSave(self):
        cursor.execute("DROP TABLE IF EXISTS meizi_meizis")  # 如果表存在则删除
        # 创建表sql语句
        createTab = """create table meizi_meizis(
                id int primary key auto_increment,
                mid varchar(10) not null,
                title varchar(50),
                picname varchar(10),
                page_url varchar(50),
                img_url varchar(50)
                ) default charset=utf8;"""
        cursor.execute(createTab)  # 执行创建数据表操作
        Mzitu.all_url('http://www.mzitu.com/all')

    def requestpic(self, url, Referer):  ##这个函数获取网页的response 然后返回
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        ua = random.choice(user_agent_list)
        headers = {'User-Agent': ua, "Referer": Referer}  ##较之前版本获取图片关键参数在这里
        content = requests.get(url, headers=headers)
        return content

    def request(self, url):  ##这个函数获取网页的response 然后返回
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content


Mzitu = mzitu()  ##实例化
# 连接数据库，需指定charset否则可能会报错
db = pymysql.connect(host="localhost", user="root", password="123", db="mysql", charset="utf8mb4")
cursor = db.cursor()  # 创建一个游标对象
Mzitu.createAndSave()

print(u'恭喜您下载完成啦！')
