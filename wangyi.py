# -*- coding: utf-8 -*-
import csv
from selenium import webdriver
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# 使用Selenium和Selenium爬取动态网页：网易云音乐歌单
# 网易云音乐歌单第一页的url
url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0'

# 用 Phantomjs接口创建一个Selenium的webDriver
driver = webdriver.PhantomJS()

# 准备好存储歌单的csw文件
# csv模块
# ‘r’：只读（缺省。如果文件不存在，则抛出错误）
# ‘w’：只写（如果文件不存在，则自动创建文件）
# ‘a’：附加到文件末尾（如果文件不存在，则自动创建文件）
# ‘r+’：读写（如果文件不存在，则抛出错误）

csv_file = open("playlist.csv", "wb")
writer = csv.writer(csv_file)
# excel打开csv文件，可以识别编码“GB2312”，但是不能识别“utf-8”
writer.writerow(['标题'.encode('GB2312'), '播放数'.encode('GB2312'), '链接'.encode('GB2312')])
# 解析每一页,直到下一页为空
while url != 'javascript:void(0)':
    # 用MebDriver加载页面
    driver.get(url)
    # 切换到内容的iframe
    driver.switch_to.frame("contentFrame")
    # 定位歌单标签
    data = driver.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')
    # 解析一页中的所有歌单
    for i in range(len(data)):
        #  获取播放量
        nb = data[i].find_element_by_class_name('nb').text
        if '万' in nb and int(nb.split('万')[0]) > 500:
            # 获取播放量大于500万的歌单的封面
            msk = data[i].find_element_by_css_selector('a.msk')
            # 把封面上的标题和链接连同播放数一起写到文件中
            print type(msk.get_attribute('title'))
            writer.writerow([msk.get_attribute('title').encode('GB2312'), nb.encode('GB2312'),
                             msk.get_attribute('href').encode('GB2312')])
    break
    # 定位下一页url,但是这里报错了
    # url = driver.find_element_by_class_name('zbtn znxt').get_attribute('href')
csv_file.close()
