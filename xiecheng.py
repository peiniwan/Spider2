# -*- coding: utf-8 -*-
import re
from pprint import pprint
import requests, json, os
from docopt import docopt
from prettytable import PrettyTable
from colorama import init, Fore
import requests


# 此程序可用于查询携程机票，查询需要指定出发日期、出发城市、目的城市！（模仿了12306火车订票查询程序）
def air_stations():
    url = 'http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?CR_2017_07_18_00_00_00'
    response = requests.get(url, verify=False)
    station = re.findall(u'([\u4e00-\u9fa5]+)\(([A-Z]+)\)', response.text)
    stations = dict(station)
    encode_stations = json.dumps(stations, encoding='UTF-8', ensure_ascii=False);
    # pprint(encode, indent=4)
    print encode_stations
    return encode_stations


fromCity = raw_input('Please input the city you want leave :')
toCity = raw_input('Please input the city you will arrive :')
tripDate = raw_input('Please input the date(Example:2017-09-27) :')

init()


class TrainsCollection:
    header = '航空公司 航班 机场 时间 机票价格 机场建设费'.split()

    def __init__(self, airline_tickets):
        self.airline_tickets = airline_tickets

    @property
    def plains(self):
        # 航空公司的总表没有找到，但是常见航空公司也不是很多就暂时用这个dict{air_company}来收集！
        # 如果strs没有查询成功，则会返回一个KeyError，表示此dict中未找到目标航空公司，则会用其英文代码显示！
        air_company = {"G5": "华夏航空", "9C": "春秋航空", "MU": "东方航空", "NS": "河北航空", "HU": "海南航空", "HO": "吉祥航空",
                       "CZ": "南方航空", "FM": "上海航空", "ZH": "深圳航空", "MF": "厦门航空", "CA": "中国国航", "KN": "中国联航"}
        for item in self.airline_tickets:
            try:
                strs = air_company[item['alc']]
            except KeyError:
                strs = item['alc']
            airline_data = [
                Fore.BLUE + strs + Fore.RESET,
                Fore.BLUE + item['fn'] + Fore.RESET,
                '\n'.join([Fore.YELLOW + item['dpbn'] + Fore.RESET,
                           Fore.CYAN + item['apbn'] + Fore.RESET]),
                '\n'.join([Fore.YELLOW + item['dt'] + Fore.RESET,
                           Fore.CYAN + item['at'] + Fore.RESET]),
                item['lp'],
                item['tax'],
            ]
            yield airline_data

    def pretty_print(self):
        # PrettyTable（）用于在屏幕上将查询到的航班信息表逐行打印到终端
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for airline_data in self.plains:
            pt.add_row(airline_data)
        print(pt)


def doit():
    headers = {
        "Cookie": "自定义",
        "User-Agent": "自定义",
    }
    arguments = {
        'from': fromCity,
        'to': toCity,
        'date': tripDate
    }

    stations = json.loads(air_stations())

    # 下面三种方法转Unicode
    # str = stations[u'北京']
    DCity1 = stations[arguments['from'].decode('utf-8')]
    ACity1 = stations[unicode(arguments['to'], 'utf-8')]
    DDate1 = arguments['date']
    url = (
        "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1={}&ACity1={}&SearchType=S&DDate1={}").format(
        DCity1, ACity1, DDate1)
    try:
        r = requests.get(url, headers=headers, verify=False)
    except Exception as e:
        print(repr(e))
    print(url)
    airline_tickets = r.json()['fis']
    TrainsCollection(airline_tickets).pretty_print()


if __name__ == '__main__':
    doit()
