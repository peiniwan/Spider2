# -*- coding: utf-8 -*-

import requests
import re
import time
from bs4 import BeautifulSoup

# 爬取豆瓣美女
# 2大熊，6小翘臀，7黑丝，3美腿，4有颜值，5大杂烩
cat = '7'
img = 'http://www.dbmeinv.com/dbgroup/show.htm?cid=' + cat
end = '/dbgroup/show.htm?cid=' + cat + '&pager_offset=10'
urls = []


def getURLs(mainURL):
    time.sleep(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    html = requests.get(mainURL).text
    soup = BeautifulSoup(html, 'html.parser')
    picURL = re.findall('<img class.*?src="(.+?\.jpg)"', html, re.S)
    for url in picURL:
        #转化高清图
        url = re.sub('bmiddle', 'large', url, 1)
        urls.append(url)
        print(url)
    asoup = soup.select('.next a')[0]['href']
    Next_page = 'http://www.dbmeinv.com' + asoup
    if asoup != end:
        getURLs(Next_page)
    else:
        print('链接已处理完毕！')
    return urls


url = getURLs(img)

i = 0
for each in url:
    pic = requests.get(each, timeout=10)
    picName = 'pictures/' + str(i) + '.jpg'
    fp = open(picName, 'wb')
    fp.write(pic.content)
    fp.close()
    i += 1

print('图片下载完成')
