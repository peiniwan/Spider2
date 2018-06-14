# -*- coding: utf-8 -*-

import re
import pymysql
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class SearchWeather():
    def __init__(self):
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.CONNECTION = pymysql.connect(host='localhost', user='root', password='123', db='mysql', charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor)

    def getcityCode(self, cityName):
        SQL = "SELECT cityCode FROM cityWeather WHERE cityName='%s'" % cityName
        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(SQL)
                self.CONNECTION.commit()
                result = cursor.fetchone()
                return result['cityCode']
        except Exception as e:
            print(repr(e))

    def getWeather(self, cityCode, cityname):
        url = 'http://www.weather.com.cn/weather/%s.shtml' % cityCode
        html = requests.get(url, headers=self.HEADERS)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        weather = "日期      天气    【温度】    风向风力\n"
        """"
        	<div id="7d" class="c7d">
								<input type="hidden" id="hidden_title" value="05月30日08时 周三  晴  33/18°C" />
                <input type="hidden" id="fc_24h_internal_update_time" value="2018053008"/>
                <input type="hidden" id="update_time" value="11:30"/>
                    <ul class="t clearfix">
                    <li class="sky skyid lv1 on">
                    <h1>30日（今天）</h1>
                    <big class="png40 d00"></big>
                    <big class="png40 n00"></big>
                    <p title="晴" class="wea">晴</p>
                    <p class="tem">
                    <span>33</span>/<i>18℃</i>
                    </p>
                    <p class="win">
                    <em>
                    <span title="北风" class="N"></span>
                    <span title="西南风" class="SW"></span>
                    </em>
                    <i><3级</i>
                    </p>
                    <div class="slid"></div>
                    </li>
                    <li class="sky skyid lv1">
                    <h1>31日（明天）</h1>
        """
        for item in soup.find("div", {'id': '7d'}).find('ul').find_all('li'):
            date, detail = item.find('h1').string, item.find_all('p')
            title = detail[0].string
            templow = detail[1].find("i").string
            temphigh = detail[1].find('span').string if detail[1].find('span') else ''
            wind, direction = detail[2].find('span')['title'], detail[2].find('i').string
            if temphigh == '':
                weather += '你好，【%s】今天白天：【%s】，温度：【%s】，%s：【%s】\n' % (cityname, title, templow, wind, direction)
            else:
                weather += (date + title + "【" + templow + "~" + temphigh + '°C】' + wind + direction + "\n")
        return weather

    def main(self, city):
        cityCode = self.getcityCode(city)
        detail = self.getWeather(cityCode, city)
        print (detail)


if __name__ == "__main__":
    weather = SearchWeather()
    weather.main(city=raw_input('请输入城市名称：'))
