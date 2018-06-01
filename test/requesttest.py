# -*- coding: utf-8 -*-
# !/usr/bin/env python

import requests as requests

# 0. 认证、状态码、header、编码、json
r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
r.status_code
# 200
print r.headers['content-type']
# 'application/json; charset=utf8'
print r.encoding
# 'utf-8'
print r.text
# u'{"type":"User"...'
print r.json()
# {u'private_gists': 419, u'total_private_repos': 77, ...}


# 1. 发起请求
URL = "http://www.bsdmap.com/"
r = requests.get(URL)
r = requests.post(URL)
r = requests.put(URL)
r = requests.delete(URL)
r = requests.head(URL)
r = requests.options(URL)

# 2. 通过URL传递参数
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://httpbin.org/get", params=payload)
print r.url
# u'http://httpbin.org/get?key2=value2&amp;key1=value1'

# 3. 返回内容
# Requests会自动解码来自服务器的内容。大多数unicode字符集都能被无缝地解码。
# 请求发出后，Requests会基于HTTP头部对响应的编码作出有根据的推测。当你访问r.text 之时，
# Requests会使用其推测的文本编码。你可以找出Requests使用了什么编码，并且能够使用 r.encoding 属性来改变它:
r = requests.get('https://github.com/timeline.json')
r.text
# '[{"repository":{"open_issues":0,"url":"https://github.com/...
print r.encoding
# 'utf-8'
r.encoding = 'ISO-8859-1'

# 4. 二进制内容
# You can also access the response body as bytes, for non-text requests:
print r.content
# b'[{"repository":{"open_issues":0,"url":"https://github.com/...

# The gzip and deflate transfer-encodings are automatically decoded for you.

# For example, to create an image from binary data returned by a request,
#  ou can use the following code:

# from PIL import Image
# from StringIO import StringIO
# print i = Image.open(StringIO(r.content))

# 5. JSON
r = requests.get('https://github.com/timeline.json')
r.json()
# [{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...
# 6. 超时
print requests.get('http://github.com', timeout=0.001)
# 7. 自定义header
import json

url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
