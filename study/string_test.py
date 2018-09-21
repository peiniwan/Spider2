# -*- coding: utf-8 -*-
# coding=utf-8
import collections
import re
import sys

import xlrd

reload(sys)
sys.setdefaultencoding('utf8')


def localSrring(excenlist):
    with open('/Users/liuyu/Documents/strings.xml', 'rb') as f:
        text = f.read()
        # print text
        pattern = re.compile('<string name="(.*?)">(.*?)</string>', re.S)
        items = re.findall(pattern, text)
        for item in items:
            # print item[0] +'-----'+item[1]
            # newstring = "<string name=\"" + item[0] + "\">" + ' ' + '</string>'
            #
            # print newstring
            for key in excenlist.items():
                if item[1] == key[0]:
                    # print key[0]
                    newstring = '<string name=' + item[0] + '>' + key[1] + '</string>'
                    print newstring


def localSrring2():
    with open('/Users/liuyu/Documents/strings.xml', 'rb') as f:
        text = f.read()
        # print text
        pattern = re.compile('<string name="(.*?)">(.*?)</string>', re.S)
        items = re.findall(pattern, text)
        list = {}

        for item in items:
            with open('/Users/liuyu/Documents/strings 2.xml', 'rb') as f2:
                text2 = f2.read()
                pattern = re.compile('<string name="(.*?)">(.*?)</string>', re.S)
                items2 = re.findall(pattern, text2)
                for item2 in items2:
                    if (item[0] == item2[0]):
                        list[item[1]] = item2[1]
        return list


def localSrring3():
    with open('/Users/liuyu/Documents/strings.xml', 'rb') as f:
        text = f.read()
        pattern = re.compile('<string name="(.*?)">(.*?)</string>', re.S)
        items = re.findall(pattern, text)
        # list = {}
        list = collections.OrderedDict()

        for item in items:
            # print item[0] + '-----' + item[1]
            newstring = "<string name=\"" + item[0] + "\">" + '@' + '</string>'
            # print newstring
            list[item[1]] = newstring
        return list


def localSrring4():
    with open('/Users/liuyu/Documents/strings_arr.xml', 'rb') as f:
        text = f.read()
        pattern = re.compile('<item>(.*?)</item>', re.S)
        items = re.findall(pattern, text)
        # list = {}
        list = collections.OrderedDict()

        for item in items:
            # print item[0] + '-----' + item[1]
            newstring = "<item>" + '@' + '</item>'
            list[item[1]] = newstring
        return list


def open_excel(file='/Users/liuyu/Documents/8.24trans.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)


# 根据索引获取Excel表格中的数据
def excel_table_byindex(file='/Users/liuyu/Documents/tk.xlsx', by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(0)  # 某一行数据
    list = {}
    row1 = table.col_values(1)  # 某一列数据
    row2 = table.col_values(2)

    for rownum in range(1, nrows):
        list[row1[rownum]] = row2[rownum];

    # for str in row1:
    #     for ko in table.col_values(4):
    #         if str != '':
    #             list[str] = ko;
    #             # print str
    return list


def excel_table_byindex2(file='/Users/liuyu/Documents/yinyu.xlsx', by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(0)  # 某一行数据
    # list = {}
    list = collections.OrderedDict()
    row1 = table.col_values(0)  # 某一列数据
    row2 = table.col_values(1)

    for rownum in range(1, nrows):
        list1 = row1[rownum].split('=')
        list2 = row2[rownum].split('=')
        # if list1[0] == list2[0]:
        if cmp(list1[0], list2[0]):
            list[list1[1].replace('\"', '')] = list2[1].replace('\"', '')
    return list


def merge_list(excenlist, excenlist2):
    list = []
    print type(excenlist2)
    for key in excenlist2.items():
        replace_string2 = key[1].replace('@', ' ')
        # print replace_string2
        for key2 in excenlist.items():
            if key[0] == key2[0]:
                # print type(key[0]),type(key2[0])
                # if replace_string2  in list:
                replace_string = key[1].replace('@', key2[1])
                list.append(replace_string)
    return list


def merge_list2(or_list, new_excenlist3):
    # print len(new_excenlist3)
    list = []
    for end in or_list:
        pattern = re.compile('<string name="(.*?)">(.*?)</string>', re.S)
        items = re.findall(pattern, end)
        print end
        # if end not in list:
        for orstring in new_excenlist3:
            pattern2 = re.compile('<string name="(.*?)">(.*?)</string>', re.S)
            items2 = re.findall(pattern2, orstring)
            # print items2[0][0]
            if items[0][0] == items2[0][0].encode('utf-8'):
                # if cmp(items[0][0], items2[0][0].encode("utf-8")):
                newstring = "<string name=\"" + items[0][0] + "\">" + items2[0][1] + '</string>'
            else:
                newstring = end
            list.append(newstring)
            break
    return list


if __name__ == "__main__":
    # excenlist = excel_table_byindex()
    # localSrring(excenlist)
    excenlist = excel_table_byindex()
    print  len(excenlist)
    for key in excenlist.items():
        print key[0], key[1]

    excenlist2 = localSrring3()
    # or_list = []
    # print  len(excenlist2)
    # for key in excenlist2.items():
    #     print key[0], key[1]
    #     # or_list.append(key[1])

    excenlist3 = merge_list(excenlist, excenlist2)
    new_excenlist3 = list(set(excenlist3))
    print len(new_excenlist3)

    for str1 in new_excenlist3:
        print str1

    # excenlist4 = localSrring4()
    # excenlist5 = merge_list(excenlist, excenlist4)
    # excenlist5 = list(set(excenlist5))
    # print len(excenlist5)

    # excenlist4 = merge_list2(or_list, new_excenlist3)
    # for str1 in excenlist4:
    #     print str1
