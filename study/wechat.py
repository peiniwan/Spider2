# -*- coding: utf-8 -*-
# coding=utf-8
from __future__ import unicode_literals

# pip install itchat    #微信
# pip install pyecharts  #数据可视化
# pip install echarts-countries-pypkg   #地图
# pip install jieba  #分词
# pip install wordcloud

import os
import re
from math import sqrt

import jieba
from PIL import Image
import itchat
from imageio import imread
from pyecharts import Bar, Map
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np


class Wechat(object):
    def __init__(self):
        self.basepath = "d:\itchat\\"

    # 微信好友头像生成
    def downFrients(self):
        my_friends = itchat.get_friends(update=True)[0:]
        for friend in my_friends[1:]:
            # 可以用此句print查看好友的微信名、备注名、性别、省份、个性签名（1：男 2：女 0：性别不详）
            # print(friend['NickName'], friend['RemarkName'], friend['Sex'], friend['Province'], friend['Signature'])
            img = itchat.get_head_img(userName=friend["UserName"])
            rstr = "[\/\\\:\*\?\"\<\>\|]"
            new_NickName = re.sub(rstr, "_", friend['NickName'])
            if os.path.isdir(self.basepath):
                pass
            else:
                os.makedirs(self.basepath)
            path = self.basepath + new_NickName + "(" + friend['RemarkName'] + ").jpg"
            try:
                with open(path, 'wb') as f:
                    f.write(img)
            except Exception as e:
                print(repr(e))
        itchat.run()
        self.save()

    def save(self):
        # path是存放好友头像图的文件夹的路径
        pathList = []
        for item in os.listdir(self.basepath):
            imgPath = os.path.join(self.basepath, item)
            pathList.append(imgPath)
        total = len(pathList)  # total是好友头像图片总数
        line = int(sqrt(total))  # line是拼接图片的行数（即每一行包含的图片数量）
        NewImage = Image.new('RGB', (128 * line, 128 * line))
        x = y = 0
        for item in pathList:
            try:
                img = Image.open(item)
                img = img.resize((128, 128), Image.ANTIALIAS)
                NewImage.paste(img, (x * 128, y * 128))
                x += 1
            except IOError:
                print("第%d行,%d列文件读取失败！IOError:%s" % (y, x, item))
                x -= 1
            if x == line:
                x = 0
                y += 1
            if (x + line * y) == line * line:
                break
        NewImage.save(self.basepath + "final.jpg")

    def get_sex(self):
        # 获取好友数据
        my_friends = itchat.get_friends(update=True)[0:]
        sex = {"male": 0, "female": 0, "other": 0}
        for item in my_friends[1:]:
            s = item["Sex"]
            if s == 1:
                sex["male"] += 1
            elif s == 2:
                sex["female"] += 1
            else:
                sex["other"] += 1
        total = len(my_friends[1:])
        print sex, total

    def get_data(self, type):
        result = []
        my_friends = itchat.get_friends(update=True)[0:]
        for item in my_friends:
            result.append(item[type])
        return result

    def friends_province(self):
        # 获取好友省份
        province = self.get_data('Province')
        # 分类
        province_distribution = {}
        for item in province:
            # 删除英文省份，因为中国地图表中没有
            if bool(re.search('[a-z]', item)):
                continue
            elif not province_distribution.__contains__(item):
                province_distribution[item] = 1
            else:
                province_distribution[item] += 1
        # 将省份名为空的删除
        province_distribution.pop('')
        # 提取地图接口需要的数据格式
        province_keys = province_distribution.keys()
        province_values = province_distribution.values()
        return province_keys, province_values

    def friends_signature(self):
        signature = self.get_data("Signature")
        wash_signature = []
        for item in signature:
            # 去除emoji表情等非文字
            if "emoji" in item:
                continue
            rep = re.compile("1f\d+\w*|[<>/=【】『』♂ω]")
            item = rep.sub("", item)
            wash_signature.append(item)

        words = "".join(wash_signature)
        wordlist = jieba.cut(words, cut_all=True)
        word_space_split = " ".join(wordlist)
        # coloring = re(Image.open("d:\\test1.jpg"))
        coloring =np.array(Image.open("d:\\test2.jpg"))
        my_wordcloud = WordCloud(background_color="white", max_words=800,
                                 mask=coloring, max_font_size=80, random_state=30, scale=2,
                                 font_path="C:/Windows/Fonts/simhei.ttf").generate(word_space_split)

        image_colors = ImageColorGenerator(coloring)
        plt.imshow(my_wordcloud.recolor(color_func=image_colors))
        plt.imshow(my_wordcloud)
        plt.axis("off")
        plt.show()


itchat.auto_login(True)
wechat = Wechat();
# wechat.downFrientsToPic()
# wechat.get_sex()
wechat.friends_signature()

# # 微信好友省份分布
# attr, value = wechat.friends_province()
# map = Map("我的微信好友分布", "@yu", width=1200, height=600)
# map.add("", attr, value, maptype='china', is_visualmap=True,
#         visual_text_color='#000')
# map.render("我的微信好友分布.html")
