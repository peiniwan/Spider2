# -*- coding: utf-8 -*-

from aip import AipOcr
# pip install aip

# 识别图片文字，使用的百度云api，可以自己申请一个
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
with open('D:\\test2.png', 'rb') as f:
    img = f.read()
    msg = client.general(img)
    for i in msg.get('words_result'):
        print(i.get('words'))
