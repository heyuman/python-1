# -*- coding: utf-8 -*-
#获取天气预报
__anthor__ = "Herman"
import json

import requests
from bs4 import BeautifulSoup
from xpinyin import Pinyin

url = 'http://www.tianqi.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
}
def getrealweather(options):
    result = {}
    pin = Pinyin()
    cityname=pin.get_pinyin(json.loads(options)['name'],"")
    geturl = url + cityname+'/'
    r = requests.get(geturl, headers=headers)
    r.encoding = 'utf-8'
    weather_soup = BeautifulSoup(r.text, from_encoding='utf-8')



