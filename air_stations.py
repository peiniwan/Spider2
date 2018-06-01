import re
from pprint import pprint

import requests

url = 'http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?CR_2017_07_18_00_00_00'
response = requests.get(url, verify=False)
station = re.findall(u'([\u4e00-\u9fa5]+)\(([A-Z]+)\)', response.text)
stations = dict(station)
pprint(stations, indent=4)