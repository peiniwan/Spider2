#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

# 安装beautifulsoup4、lxml、html5lib
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# soup = BeautifulSoup(open('index.html'))
soup = BeautifulSoup(html, "lxml")
# 格式化打印出了它的内容
print soup.prettify()

# html = <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

