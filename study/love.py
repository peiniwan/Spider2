# -*- coding: utf-8 -*-

import time

# 画心
words = raw_input('Please input the words you want to say!:')
# 例子：words = "Dear lili, Happy Valentine's Day! Lyon Will Always Love You Till The End! ♥ Forever!  ♥"
for item in words.split():
    # 要想实现打印出字符间的空格效果，此处添加：item = item+' '
    letterlist = []  # letterlist是所有打印字符的总list，里面包含y条子列表list_X
    for y in range(12, -12, -1):
        list_X = []  # list_X是X轴上的打印字符列表，里面装着一个String类的letters
        letters = ''  # letters即为list_X内的字符串，实际是本行要打印的所有字符
        for x in range(-30, 30):  # *是乘法，**是幂次方
            expression = ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3
            if expression <= 0:
                letters += item[(x - y) % len(item)]
            else:
                letters += ' '
        list_X.append(letters)
        letterlist += list_X
    print('\n'.join(letterlist))
    time.sleep(1.5);
