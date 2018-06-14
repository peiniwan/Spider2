#!/usr/bin/env python
# -*- coding:utf-8 -*-
# python抓取bing主页所有背景图片
from gevent import monkey

monkey.patch_all()

import gevent
import requests
import json
import os
import re
import datetime

from threadpool import ThreadPool
from threadpool import makeRequests
from BeautifulSoup import BeautifulSoup

g_real_url = []


def elapse(func):
    def deco(*args, **kwargs):
        starttime = datetime.datetime.now()
        func(*args, **kwargs)
        endtime = datetime.datetime.now()
        print "elapse time: " + str((endtime - starttime).seconds) + " seconds"

    return deco


def get_background_info(url):
    re = requests.get(url)
    re_content = json.loads(re.content)
    url = re_content["images"][0]["url"]
    name = re_content["images"][0]["enddate"]
    download(url, name)


def download(url, name):
    dest = r'd:\\biying'
    if os.path.exists(dest) is False:
        os.makedirs(dest)
    re = requests.get(url)
    raw = re.content
    path = dest + os.path.sep + name + ".jpg"
    if os.path.exists(path) is False:
        with open(dest + os.path.sep + name + ".jpg", "wb") as f:
            f.write(raw)


def rename(str):
    replace_str = "$"
    pattern = re.compile('[/\\\\:*?<>|"]')
    m = pattern.search(str)
    if m is not None:
        re_s = str.replace(m.group(), replace_str)
        if pattern.search(re_s) is not None:
            re_s = rename(re_s)
        return re_s
    else:
        return str


def get_background():
    for i in range(17):
        root_url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=" + str(i) + "&n=1&mkt=zh-cn"
        get_background_info(root_url)


def get_one_month_background(year, month):
    print 'get image %s %s' % (year, month)
    url = "http://www.istartedsomething.com/bingimages/?m=" + str(month) + "&y=" + str(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.content)
    target = soup.find('table').findAllNext(attrs={'href': re.compile(r"-cn")})

    download_task = []

    for t in target:
        title = t.get('title')
        date = t.get('href')[1:]
        url = t.img.get('data-original')
        real_url = 'http://www.istartedsomething.com/bingimages/cache/' + url.split('=')[1][:-2]

        file_name = date + "_" + rename(title)
        # if title.find(u"(©") != -1:
        #     file_name = date + "_" + title.split(u'(©')[0]
        # if title.find(u"--") != -1
        #     file_name = date + "_" + title.split(u'--')[0]

        download_task.append((real_url, file_name))

    # download one by one
    # for tu in download_task:
    #     download(tu[0], tu[1])

    # download by thread pool
    # download_by_threadpool(download_task)
    # return download_task

    return g_real_url.extend(download_task)


@elapse
def get_background_new(y=None):
    print "get_background_new start"
    task_list = []
    if y is None:
        for y in range(2009, 2017):
            for m in range(1, 13):
                if y <= 2009 and m <= 6:
                    continue
                task_list.append((y, m))
    else:
        for m in range(1, 13):
            if y <= 2009 and m <= 6:
                continue
            task_list.append((y, m))

    real_url_list = []
    # get one month one by one
    # for task in task_list:
    #     real_url_list.extend(get_one_month_background(task[0], task[1]))

    # by thread pool
    get_one_month_by_threadpool(task_list)

    # download_by_threadpool(real_url_list)
    download_by_threadpool(g_real_url)
    # gevent_wrapper(g_real_url)


def download_by_threadpool(download_task):
    size = 50
    pool = ThreadPool(size)
    # print [([t[0], t[1]]) for t in download_task]
    requests = makeRequests(download, [([t[0], t[1]], None) for t in download_task])
    [pool.putRequest(req) for req in requests]
    pool.wait()


def get_one_month_by_threadpool(tasks):
    size = 12
    pool = ThreadPool(size)
    requests = makeRequests(get_one_month_background, [([t[0], t[1]], None) for t in tasks])
    [pool.putRequest(req) for req in requests]
    pool.wait()


@elapse
def gevent_wrapper(tasks):
    ll = []
    for i in tasks:
        ll.append(gevent.spawn(download, i[0], i[1]))
    gevent.joinall(ll)


if __name__ == '__main__':
    # get_background()
    # get_background_new(2015)
    # get_background_new()
    get_one_month_background(2016, 9)
    # gevent_wrapper('xxx')
