# coding: utf-8
import json

import requests
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
}
r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, from_encoding='utf-8')


# 豆瓣电影首页数据
def frist():
    result = {}
    screening = soup.select('.screening-bd .ui-slide-content .ui-slide-item')
    if len(soup.select('.screening-bd .ui-slide-content .ui-slide-item')):
        screening_data = []
        for item in screening:
            obj = {}
            if len(item.select('ul')) != 0:
                obj['cover'] = item.select('.poster a img')[0]['src']
                obj['url'] = item.select('.poster a')[0]['href']
                obj['title'] = item.select('.title a')[0].string
                if len(item.select('.rating .subject-rate')) != 0:
                    obj['rating'] = item.select('.rating .subject-rate')[0].string
                else:
                    obj['rating'] = '0.0'
                obj['ticket'] = item.select('.ticket_btn span a')[0]['href']
                screening_data.append(obj)
        hotmovie = requests.get(
            'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0').text
        result['screening_data'] = screening_data
        result['hotmovie_data'] = json.loads(hotmovie)['subjects']
    return json.dumps(result)


# 豆瓣电影电影详情数据
def detailed_func(options):
    result = {}
    detailed_url = json.loads(options)['url']
    print(options)
    detailed_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
    }
    detailed = requests.get(detailed_url, headers=detailed_headers)
    detailed.encoding = 'utf-8'
    detailed_soup = BeautifulSoup(detailed.text, from_encoding='utf-8')
    # 影片信息
    if len(detailed_soup.select('#info .pl')) > 0:
        info = []
        num=0
        test = detailed_soup.select('#info .pl')
        for item in (detailed_soup.select('#info .pl')):
            value = ''
            values = {}
            if item.next_sibling != ' ':
                value = item.next_sibling
            else:
                if len(item.find_next_siblings('span')) > 0:
                    value = item.find_next_siblings('span')[0].string
            values = item.string + value
            if len(item.find_next_siblings('span', 'attrs')) > 0:
                index = 0
                for sibling in item.find_next_siblings('span', 'attrs')[0].children:
                    index += 1
                    if index < 10:
                        if sibling.string:
                            values = values + sibling.string
            num=num+1
            info.append(values)
        info.pop()
        result['info'] = info
    # 影片标题
    if len(detailed_soup.select('h1 span')) > 0:
        title = ''
        for item in detailed_soup.select('h1 span'):
            title = title + item.string
        result['title'] = title
    # 剧情简介
    if len(detailed_soup.select('.related-info .indent span')) > 0:
        synopsis = detailed_soup.select('.related-info .indent span')[0].text.lstrip()
        result['synopsis'] = synopsis
    # 影人
    if len(detailed_soup.select('.celebrities .celebrities-list li')) > 0:
        celebrities = detailed_soup.select('.celebrities .celebrities-list li')
        actors = []
        for item in celebrities:
            actor = {}
            if len(item.select('.avatar')) > 0:
                actor['img'] = item.select('.avatar')[0]['style'].lstrip('background-image: url(').rstrip(')')
            if len(item.select('.info .name .name')) > 0:
                #演员的名字和演员简介url
                actor["url"]=item.select(".info .name a")[0]['href']
                actor['name'] = item.select('.info .name .name')[0].string
            if len(item.select('.info .role')) > 0:
                actor['status'] = item.select('.info .role')[0].string
            actors.append(actor)
        result['actors'] = actors
    # 剧照列表
    if len(detailed_soup.select('.related-pic .related-pic-bd li')) > 0:
        related = detailed_soup.select('.related-pic .related-pic-bd li')
        photolist = []
        for item in related:
            if len(item.select('.related-pic-video'))>0:
                photolist.append(item.a['style'].split("(")[1].split(")")[0])
            else:
                photolist.append(item.a.img['src'])
            # photolist.append(items)
        result['photoList'] = photolist
    # 评分
    if len(detailed_soup.select('.rating_self strong')) > 0:
        grade = detailed_soup.select('.rating_self strong')[0].string
        result['grade'] = grade
    # 相关电影
    if len(detailed_soup.select('.recommendations-bd dl')) > 0:
        aboutlist = detailed_soup.select('.recommendations-bd dl')
        aboutmovies = []
        for item in aboutlist:
            movie = {
                'cover': item.dt.a.img['src'],
                'title': item.dd.a.text,
                'url':item.dd.a['href']
            }
            aboutmovies.append(movie)
        result['aboutmovies'] = aboutmovies
    # 影片评论
    if len(detailed_soup.select('#hot-comments .comment-item')) > 0:
        commentlist = detailed_soup.select('#hot-comments .comment-item')
        comment = []
        for item in commentlist:
            user = {}
            user['nickname'] = item.select('.comment .comment-info a')[0].text
            user['time'] = item.select('.comment .comment-info .comment-time ')[0].text.lstrip()
            user['like'] = item.select('.comment .comment-vote .votes')[0].text
            user['content'] = item.select('.comment p')[0].text
            comment.append(user)
        result['comment'] = comment
    # 返回数据结果
    result['cover'] = json.loads(options)['cover']
    return json.dumps(result)


# 豆瓣电影搜索
def search_func(value):
    response = requests.get('https://movie.douban.com/j/subject_suggest?q=' + value, headers=headers)
    response.encoding = 'utf-8'
    return json.dumps(response.json())


#电影演员详情介绍
def detailed_actor_func(options):
    result = {}
    detailed_url = json.loads(options)['url']
    print(options)
    detailed_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
    }
    #将内容获取到
    detailed = requests.get(detailed_url, headers=detailed_headers)
    detailed.encoding = 'utf-8'
    detailed_soup = BeautifulSoup(detailed.text, from_encoding='utf-8')
    # 演员名字
    if len(detailed_soup.select('h1')) > 0:
        title = detailed_soup.select('h1')
        title =title[0].text.lstrip()
    else:
        title="未知"
    result['title'] = title
    # 演员头像
    if len(detailed_soup.select('.pic a')) > 0:
        actors_head = detailed_soup.select('.pic a')[0]['href']
        result['actors_head'] = actors_head
    else:
        #传进来的值
        result['actors_head'] = json.loads(options)['cover']

    # 演员信息
    if len(detailed_soup.select('.info li')) > 0:
        info = []
        #使用下标时必须是enumerate()枚举
        for i,item in enumerate(detailed_soup.select('.info li')):

            value =item.get_text().strip()
            value=''.join(value.split(' '))
            value=''.join(value.split('\n'))
            text=value.split(':', 1)[0]
            print(value)
            info.append(value)
        result['info'] = info
    # 演员简介
    if len(detailed_soup.select('#intro .bd .all.hidden')) > 0:
        actors = detailed_soup.select('#intro .bd .all.hidden')
        print(actors)
        actors = detailed_soup.select('#intro .bd .all.hidden')[0].text.strip()
    else:
        actors="暂无简介"
    result['actors'] = actors
    #演员相关照片
    if len(detailed_soup.select('#photos .pic-col5 li'))>0:
        photos=[]
        index = 0
        photo_list=(detailed_soup.select('#photos .pic-col5 li'))
        for item in photo_list:
            index= +1
            if index < 5:
               photos.append(item.a.img['src'])
        result['photos']=photos
    # 演员相关电影
    if len(detailed_soup.select('#recent_movies .list-s li')) > 0:
        aboutmovies = []
        index = 0
        movies_list = detailed_soup.select('#recent_movies .list-s li')
        for item in movies_list:
            index = +1
            print(item.select('.info a'))
            if index < 5:
                title=item.select('.info a')[0].text.strip()
                movie = {
                    'cover': item.a.img['src'],
                    'title': title,
                    'url': item.a['href']
                }
                aboutmovies.append(movie)
        result['aboutmovies'] = aboutmovies
    return json.dumps(result)
