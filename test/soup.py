#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import bs4
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
# print soup.prettify()

# 打印tag
print soup.title
# <title>The Dormouse's story</title>
print soup.head
# <head><title>The Dormouse's story</title></head>
# 它查找的是在所有内容中的第一个符合要求的标签
print soup.a
# <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
print soup.p
print soup.name
print soup.head.name
# [document]
# head
print soup.p.attrs
# {'class': ['title'], 'name': 'dromouse'}
print soup.p['class']
# ['title']
print soup.p.get('class')
# 跟上面一样
soup.p['class'] = "newClass"
print soup.p
# <p class="newClass" name="dromouse"><b>The Dormouse's story</b></p>
# del soup.p['class']


# 打印NavigableString
# 获取标签内部的文字
print soup.p.string
# The Dormouse's story
# 检查类型
print type(soup.p.string)
# <class 'bs4.element.NavigableString'>


# BeautifulSoup 对象表示的是一个文档的全部内容.大部分时候,
# 可以把它当作 Tag 对象，是一个特殊的 Tag，我们可以分别获取它的类型，名称
print type(soup.name)
# <type 'unicode'>
print soup.name
# [document]
print soup.attrs
# {} 空字典

# Comment 对象是一个特殊类型的 NavigableString 对象，其实输出的内容仍然不包括注释符号
print soup.a
print soup.a.string
print type(soup.a.string)
# <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
#  Elsie
# <class 'bs4.element.Comment'>
# a 标签里的内容实际上是注释，但是如果我们利用 .string 来输出它的内容，我们发现它已经把注释符号去掉了
# 打印输出下它的类型，发现它是一个 Comment 类型，所以，我们在使用前最好做一下判断
if type(soup.a.string) == bs4.element.Comment:
    print soup.a.string

# 一·遍历文档树
# （1）直接子节点
# tag 的 .content 属性可以将tag的子节点以列表的方式输出
print soup.head.contents
# [<title>The Dormouse's story</title>]
# 输出方式为列表，我们可以用列表索引来获取它的某一个元素
print soup.head.contents[0]
# <title>The Dormouse's story</title>

# .children是个list
# <listiterator object at 0x7f71457f5710>
for child in soup.body.children:
    print child

# （2）所有子孙节点
# .contents 和 .children 属性仅包含tag的直接子节点，
# .descendants 属性可以对所有tag的子孙节点进行递归循环
for child in soup.descendants:
    print child

# （3）节点内容
# 如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。
# 如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容
print soup.head.string
# The Dormouse's story
print soup.title.string
# The Dormouse's story
print soup.html.string
# None

# （4）多个内容
# .strings获取多个内容，不过需要遍历获取
for string in soup.strings:
    print(repr(string))
    # u"The Dormouse's story"
    # u'\n\n'
    # u"The Dormouse's story"
    # u'\n\n'
    # u'Once upon a time there were three little sisters; and their names were\n'
    # u'Elsie'
    # u',\n'
# 使用 .stripped_strings 可以去除多余空白内容
for string in soup.stripped_strings:
    print(repr(string))
    # u"The Dormouse's story"
    # u"The Dormouse's story"
    # u'Once upon a time there were three little sisters; and their names were'
    # u'Elsie'
    # u','
    # u'Lacie'
    # u'and'
    # u'Tillie'
    # u';\nand they lived at the bottom of a well.'
    # u'...'

# （5）父节点
p = soup.p
print p.parent.name
# body
content = soup.head.title.string
print content.parent.name
# title

# （6）全部父节点
content = soup.head.title.string
for parent in content.parents:
    print parent.name
# title
# head
# html
# [document]

# （7）兄弟节点
# 兄弟节点可以理解为和本节点处在统一级的节点，
# .next_sibling 属性获取了该节点的下一个兄弟节点，
# .previous_sibling 则与之相反，如果节点不存在，则返回 None
# 注意：实际文档中的tag的 .next_sibling 和 .previous_sibling 属性通常是字符串或空白，
# 因为空白或者换行也可以被视作一个节点，所以得到的结果可能是空白或者换行
print soup.p.next_sibling
#       实际该处为空白
print soup.p.prev_sibling
# None   没有前一个兄弟节点，返回 None
print soup.p.next_sibling.next_sibling
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
# 下一个节点的下一个兄弟节点是我们可以看到的节点

# （8）全部兄弟节点
# 通过 .next_siblings 和 .previous_siblings 属性可以对当前节点的兄弟节点迭代输出
for sibling in soup.a.next_siblings:
    print(repr(sibling))
    # u',\n'
    # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    # u' and\n'
    # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
    # u'; and they lived at the bottom of a well.'
    # None

# （9）前后节点
# 与 .next_sibling  .previous_sibling 不同，它并不是针对于兄弟节点，而是在所有节点，不分层次
print soup.head.next_element
# <title>The Dormouse's story</title>

# （10）所有前后节点
# 通过 .next_elements 和 .previous_elements 的迭代器就可以向前或向后访问文档的解析内容,就好像文档正在被解析一样
# for element in last_a_tag.next_elements:
#     print(repr(element))
# # u'Tillie'
# # u';\nand they lived at the bottom of a well.'
# # u'\n\n'
# # <p class="story">...</p>
# # u'...'
# # u'\n'
# # None

# 二.搜索文档树
# （1）find_all( name , attrs , recursive , text , **kwargs )
# find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件

# 1）name 参数
# name 参数可以查找所有名字为 name 的tag,字符串对象会被自动忽略掉
print soup.find_all('b')
# [<b>The Dormouse's story</b>]
# 找出所有以b开头的标签,
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
print soup.find_all(["a", "b"])
# True 可以匹配任何值,下面代码查找到所有的tag,但是不会返回字符串节
for tag in soup.find_all(True):
    print(tag.name)


# 这个方法返回 True 表示当前元素匹配并且被找到,如果不是则反回 False
# 下面方法校验了当前元素,如果包含 class 属性却不包含 id 属性,那么将返回 True:
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


# 将这个方法作为参数传入 find_all() 方法,将得到所有<p>标签:
soup.find_all(has_class_but_no_id)

# 2）keyword 参数
# 如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字tag的属性来搜索,
# 如果包含一个名字为 id 的参数,Beautiful Soup会搜索每个tag的”id”属性
soup.find_all(id='link2')
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
# 如果传入 href 参数,Beautiful Soup会搜索每个tag的”href”属性
soup.find_all(href=re.compile("elsie"))
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
# 使用多个指定名字的参数可以同时过滤tag的多个属性
soup.find_all(href=re.compile("elsie"), id='link1')
# [<a class="sister" href="http://example.com/elsie" id="link1">three</a>]
# 用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
soup.find_all("a", class_="sister")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# 3）text 参数
# 通过 text 参数可以搜搜文档中的字符串内容.与 name 参数
# 的可选值一样, text 参数接受 字符串 , 正则表达式 , 列表, True
soup.find_all(text="Elsie")
# [u'Elsie']
soup.find_all(text=["Tillie", "Elsie", "Lacie"])
# [u'Elsie', u'Lacie', u'Tillie']
soup.find_all(text=re.compile("Dormouse"))
[u"The Dormouse's story", u"The Dormouse's story"]

# 4）limit 参数
# 使用 limit 参数限制返回结果的数量
soup.find_all("a", limit=2)
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

# 5）recursive 参数
# 调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,
# 如果只想搜索tag的直接子节点,可以使用参数 recursive=False .
# <html>
#  <head>
#   <title>
#    The Dormouse's story
#   </title>
#  </head>
# ...
soup.html.find_all("title")
# [<title>The Dormouse's story</title>]
soup.html.find_all("title", recursive=False)
# []


# （2）find( name , attrs , recursive , text , **kwargs )
# 它与 find_all() 方法唯一的区别是 find_all() 方法的返回结果是值包含一个元素的列表,
# 而 find() 方法直接返回结果,返回第一个符合条件的


# 三.CSS选择器
# 在写 CSS 时，标签名不加任何修饰，类名前加点，id名前加 #，
# 在这里我们可以利用类似的方法来筛选元素，用到的方法是 soup.select()，返回类型是 list
# （1）通过标签名查找
print soup.select('title')
# [<title>The Dormouse's story</title>]
print soup.select('a')
# （2）通过类名查找
print soup.select('.sister')
# （3）通过 id 名查找
print soup.select('#link1')
# （4）组合查找
# 查找 p 标签中，id 等于 link1的内容，二者需要用空格分开
print soup.select('p #link1')
# 直接子标签查找
print soup.select("head > title")
# [<title>The Dormouse's story</title>]
# （5）属性查找
# 属性需要用中括号括起来
print soup.select('a[class="sister"]')
print soup.select('a[href="http://example.com/elsie"]')
# 属性仍然可以与上述查找方式组合，不在同一节点的空格隔开，同一节点的不加空格
print soup.select('p a[href="http://example.com/elsie"]')
# 以上的 select 方法返回的结果都是列表形式，可以遍历形式输出，然后用 get_text() 方法来获取它的内容。
soup = BeautifulSoup(html, 'lxml')
print type(soup.select('title'))
print soup.select('title')[0].get_text()

for title in soup.select('title'):
    print title.get_text()
