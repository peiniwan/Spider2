#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 返回 pattern 对象
import re
import string

# 将正则表达式编译成 Pattern 对象，注意 hello 前面的 r 的意思是 “原生字符串”
pattern = re.compile(r'hello')

# 使用 re.match 匹配文本，获得匹配结果，无法匹配时将返回 None
result1 = re.match(pattern, 'hello')
result2 = re.match(pattern, 'helloo CQC!')
result3 = re.match(pattern, 'helo CQC!')
result4 = re.match(pattern, 'hello CQC!')
# hello
# hello
# 3 匹配失败！
# hello

# 如果 1 匹配成功
if result1:
    # 使用 Match 获得分组信息
    print result1.group()
else:
    print '1 匹配失败！'

# 如果 2 匹配成功
if result2:
    # 使用 Match 获得分组信息
    print result2.group()
else:
    print '2 匹配失败！'

# 如果 3 匹配成功
if result3:
    # 使用 Match 获得分组信息
    print result3.group()
else:
    print '3 匹配失败！'

# 如果 4 匹配成功
if result4:
    # 使用 Match 获得分组信息
    print result4.group()
else:
    print '4 匹配失败！'

# 匹配如下内容：单词 + 空格 + 单词 + 任意字符
m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')

print "m.string:", m.string
print "m.re:", m.re
print "m.pos:", m.pos
print "m.endpos:", m.endpos
print "m.lastindex:", m.lastindex
print "m.lastgroup:", m.lastgroup
print "m.group():", m.group()
print "m.group(1,2):", m.group(1, 2)
print "m.groups():", m.groups()
print "m.groupdict():", m.groupdict()
print "m.start(2):", m.start(2)
print "m.end(2):", m.end(2)
print "m.span(2):", m.span(2)
print r"m.expand(r'\g \g\g'):", m.expand(r'\2 \1\3')

### output ###
# m.string: hello world!
# m.re:
# m.pos: 0
# m.endpos: 12
# m.lastindex: 3
# m.lastgroup: sign
# m.group(1,2): ('hello', 'world')
# m.groups(): ('hello', 'world', '!')
# m.groupdict(): {'sign': '!'}
# m.start(2): 6
# m.end(2): 11
# m.span(2): (6, 11)
# m.expand(r'\2 \1\3'): world hello!


pattern = re.compile(r'world')
# 使用 search() 查找匹配的子串，不存在能匹配的子串时将返回 None
# 这个例子中使用 match() 无法成功匹配
match = re.search(pattern, 'hello world!')
if match:
    # 使用 Match 获得分组信息
    print match.group()
### 输出 ###
# world


pattern = re.compile(r'\d+')
print re.split(pattern, 'one1two2three3four4')

### 输出 ###
# ['one', 'two', 'three', 'four', '']

# 搜索 string，以列表形式返回全部能匹配的子串。
pattern = re.compile(r'\d+')
print re.findall(pattern, 'one1two2three3four4')

### 输出 ###
# ['1', '2', '3', '4']

# 搜索 string，返回一个顺序访问每一个匹配结果（Match 对象）的迭代器
pattern = re.compile(r'\d+')
for m in re.finditer(pattern, 'one1two2three3four4'):
    print m.group(),

### 输出 ###
# 1 2 3 4


pattern = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'
print re.sub(pattern, r'\2 \1', s)


def func(m):
    return m.group(1).title() + ' ' + m.group(2).title()


print re.sub(pattern, func, s)

### output ###
# say i, world hello!
# I Say, Hello World!
