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
#获取当前天气
def getrealweather(options):
    result = {}
    pin = Pinyin()
    cityname=pin.get_pinyin(json.loads(options)['name'],"")
    geturl = url + cityname+'/'
    try:
        r = requests.get(geturl, headers=headers)
        result["status"] = "ok"
        r.encoding = 'utf-8'
        weather_soup = BeautifulSoup(r.text, from_encoding='utf-8')
        if len(weather_soup.select('.weather_info'))>0:
            # 获取城市图片
            result["img"]=weather_soup.select('.weather_info dt img')[0]['src']
            # 获取城市名称
            result["name"]=weather_soup.select('.weather_info .name h2')[0].string
            #获取week
            result["week"]=weather_soup.select('.weather_info .week')[0].string
            # weather
            result["weather"] = weather_soup.select('.weather_info .weather img')[0]['src']
            # shidu湿度
            if len(weather_soup.select('.weather_info .shidu b')) >0:
                shidu=[]
                soup= weather_soup.select('.weather_info .shidu b')
                for item in soup:
                    value = item.get_text().strip()
                    shidu.append(value)
                result["shidu"]=shidu
            #kongqi质量
            if len(weather_soup.select('.weather_info .kongqi')) > 0:
                kongqi = []
                kongq = weather_soup.select('.weather_info .kongqi h5')[0].get_text().strip()
                pm25=weather_soup.select('.weather_info .kongqi h6')[0].get_text().strip()
                kongqi.append(kongq)
                kongqi.append(pm25)
                result["kongqi"] = kongqi
            return json.dumps(result)
    except:
        result["status"] = "failed"
        return json.dumps(result)




