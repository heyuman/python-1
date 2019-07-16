# -*- coding: utf-8 -*-
#获取天气预报
__anthor__ = "Herman"
import json

import requests
from bs4 import BeautifulSoup
from xpinyin import Pinyin
from bs4 import SoupStrainer

url = 'http://www.tianqi.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
}
def gethistoryweather(options):
    '''
    获取一周的历史数据
    :param options: 传入的城市名称
    :return: 返回一个json结果
    '''
    result = {}
    pin = Pinyin()#文字转拼音
    post_cityname=json.loads(options)['name']
    pycityname = pin.get_pinyin(post_cityname, "")
    geturl = url + pycityname + '/'
    try:
        r = requests.get(geturl, headers=headers)
        r.encoding = 'utf-8'
        class_left = SoupStrainer(class_="left")# 帅选出class_="right"的内容，节约内存---历史的数据
        soup_left = BeautifulSoup(r.text, parse_only=class_left, from_encoding='utf-8')
        class_right = SoupStrainer(class_="right")  # 帅选出class_="right"的内容，节约内存---历史的数据
        soup_right = BeautifulSoup(r.text, parse_only=class_right, from_encoding='utf-8')
        cityweeks = soup_right.select('.top h1')[0].string  # 获取城市名称
        cityname = cityweeks.split("天气")[0]
        if cityname != post_cityname:
            result["status"] = "failed"
            result["errMg"] = "请输入正确的城市名！"
            return json.dumps(result)
        result["cityname"] = cityname
        temdiff=soup_left.select('.weather_info .weather span')[0].stripped_strings#标签本身有内容，加上标签内还有标签，使用这个函数
        weather_low_high=[]
        for string in temdiff:
            weather_low_high.append(string)
        if len(soup_left.select('.weather_info'))>0:
            realday={
                "img": soup_left.select('.weather_info dt img')[0]['src'],
                "name": soup_left.select('.weather_info .name h2')[0].string,
                "realtem": soup_left.select('.weather_info .weather p')[0].get_text(),
                "week":soup_left.select('.weather_info .week')[0].string,
                "weatherimg":soup_left.select('.weather_info .weather img')[0]['src'],
                "weather":weather_low_high,
                "kongq":soup_left.select('.weather_info .kongqi h5')[0].get_text().strip(),
                "pm":soup_left.select('.weather_info .kongqi h6')[0].get_text().strip()
            }
            shidu = []
            for item in soup_left.select('.weather_info .shidu b'):
                value = item.get_text().strip()
                shidu.append(value)
            realday["shidu"]=shidu
            print(type(realday))
            result["realday"] = realday
        days = []
        for i in range(0,len(soup_right.select(".week li"))):
            print(i)
            day ={
                "temdate" : soup_right.select(".week li")[i].b.string,
                "temweekday" : soup_right.select(".week li")[i].span.string,
                "temimg" : soup_right.select(".week li")[i].img["src"],
                "weather":soup_right.select(".txt.txt2 li")[i].string,
                "hightem":soup_right.select(".zxt_shuju li")[i].span.string,
                "lowtem": soup_right.select(".zxt_shuju li")[i].b.string,
                "wind":soup_right.select("ul:nth-of-type(3) li")[i].string #获取风速'''
            }
            days.append(day)
        result["days"] = days
        result["status"] = "ok"
        return json.dumps(result)
    except:
        result["status"] = "failed"
        return json.dumps(result)