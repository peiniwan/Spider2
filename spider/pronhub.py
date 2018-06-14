# -*- coding: utf-8 -*-
import datetime
import os
import re
import urllib2

to_find_string = "https://bd.phncdn.com/videos/"
big_path = ""


def save_file(this_download_url, path):
    print"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    time1 = datetime.datetime.now()
    print str(time1)[:-7],
    if (os.path.isfile(path)):
        file_size = os.path.getsize(path) / 1024 / 1024
        print "File " + path + " (" + str(file_size) + "Mb) already exists."
        return
    else:
        print "Downloading " + path + "..."
        f = urllib2.urlopen(this_download_url)
        data = f.read()
        with open(path, "wb") as code:
            code.write(data)
        time2 = datetime.datetime.now()
        print str(time2)[:-7],
        print path + " Done."
        use_time = time2 - time1
        print "Time used: " + str(use_time)[:-7] + ", ",
        file_size = os.path.getsize(path) / 1024 / 1024
        print "File size: " + str(file_size) + " MB, Speed: " + str(file_size / (use_time.total_seconds()))[:4] + "MB/s"


def download_the_av(url):
    req = urllib2.Request(url)
    content = urllib2.urlopen(req).read()


    while len(content) < 100:
        print"try again..."
        content = urllib2.urlopen(req).read()
    print "All length:" + str(len(content))

    title_begin = content.find("<title>")
    title_end = content.find("</title>")
    title = content[title_begin + 7:title_end - 14]
    title = title.replace('/', '_')
    title = filter(lambda x: x in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ _-", title)

    quality = ['720', '480', '240']
    for i in quality:
        find_position = content.find("\"quality\":\"" + i + "\"")
        if find_position > 0:
            print "Quality: " + i + "P"
            break
    to_find = content[find_position:find_position + 4000]

    pattern = re.compile(r"\"videoUrl\":\"[^\"]*\"")
    match = pattern.search(to_find)
    if match:
        the_url = match.group()
    the_url = the_url[12:-1]  # the real url
    the_url = the_url.replace("\\/", "/")
    save_file(the_url, big_path + title + ".mp4")


urls = ["https://www.pornhub.com/view_video.php?viewkey=ph593259dab92e1",
        "https://www.pornhub.com/view_video.php?viewkey=ph5ac988c475e94"]
print len(urls),
print " videos to download..."
count = 0

for url in urls:
    print count
    count += 1
    download_the_av(url)
print "All done"
