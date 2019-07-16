# -*- coding: utf-8 -*-
__anthor__ = "Herman"
'''
1.<class 'bs4.element.ResultSet'>  这里是字典外套了一个列表  textPid = pid[0]
2.<class 'bs4.element.Tag'>   print(textPid.get_text())

'''
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("index2.html",encoding="utf-8"),features="lxml")

# print(soup)
'''.xx只能选到第一个,bs4.element.Tag'''
# print(soup.a)
# print(type(soup.a))
# print(soup.img['src'])
'''只有单个时才能用。string,不然都是none并且只能是通过.tag便签来获取,而且只能取到第一个，'''
'''多个节点soup.find_all('a'),得到的结果是list；如果一个tag仅有一个子节点,那么这个tag也可以使用 .string 方法'''
'''如果tag中包含多个字符串 [2] ,可以使用 .strings 来循环获取:'''
# print(soup.span.string)
# print(soup.find_all('span'))
# print(soup.find_all('span')[1].string)
# print(soup.find_all('span')[0])

'''
.contents 和 .children
tag的 .contents 属性可以将tag的子节点以列表的方式输出:
不能直接print(soup_img.children)
descendants是子孙节点
'''
# soup_img=soup.span
# for child in soup_img.children :
#     print(child)
# for descendants in soup_img.descendants:
#     print(descendants)

'''.strings 和 stripped_strings
.stripped_strings 可以去除多余空白内容:'''
# for string in soup.strings:
#     print(repr(string))

# for string in soup.stripped_strings:
#     print(string)

'''
.parent
通过 .parent 属性来获取某个元素的父节点.在例子“爱丽丝”的文档中,<head>标签是<title>标签的父节点:'''
# soup_title=soup.title
# print(soup_title)
# print(soup_title.parent)
# print(type(soup_title.parent)) #<class 'bs4.element.Tag'>

'''兄弟节点
使用 .next_sibling（下一个兄弟节点，同级最后一个没有这个属性） 和 .previous_sibling(上一个兄弟节点，同级第一个没有这个属性) 属性来查询兄弟节点
 .next_siblings 和 .previous_siblings 属性可以对当前节点的兄弟节点迭代输出--记得是不含自己的:
prettify--是美化文档
'''
# sibling_soup=BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>",features='lxml')
# # print(sibling_soup.prettify())
#
# print(sibling_soup.b.next_sibling)
# print(sibling_soup.c.previous_sibling)
# for sibling in soup.a.next_siblings:
#     print(repr(sibling))
# for sibling in soup.find(id='link3').previous_siblings:
#     print(repr(sibling))

''' find() 和 find_all() .其它方法的参数和用法类似,请读者举一反三.
 find_all()返回的是列表， find()返回的是直接结果
 
再以“爱丽丝”文档作为例子,'''
#soup_find = BeautifulSoup(open("index2.html",encoding="utf-8"),features="lxml")
# print(type(soup_find.find_all('b')))#<class 'bs4.element.ResultSet'>
# for b in soup_find.find_all('b'):
#     print(type(b))#<class 'bs4.element.Tag'>
'''find_all()也可以用正则表达式'''
# import re
# for tag in soup_find.find_all(re.compile("^b")):
#     if len(tag.find_all("a"))>0:
#         for a in tag.find_all("a"):
#             # print(a)
#             print(a["href"])
#     print(tag.name)

'''方法
如果包含 class 属性却不包含 id 属性,那么将返回 True:
has_attr方法
'''
# soup_find = BeautifulSoup(open("index2.html",encoding="utf-8"),features="lxml")
# def has_class_but_no_id(tag):
#     return tag.has_attr('class') and not tag.has_attr('id')
# #print(soup_find.find_all(has_class_but_no_id))
# for has_class in soup_find.find_all(has_class_but_no_id):
#     print(has_class)

'''find_all( name , attrs , recursive , text , **kwargs )细节
name 参数可以查找所有名字为 name 的tag,字符串对象会被自动忽略掉.
attrs 参数定义一个字典参数来搜索包含特殊属性的tag:
text 参数接受 字符串 , 正则表达式 , 列表, True 
'''
# soup = BeautifulSoup(open("index2.html",encoding="utf-8"),features="lxml")
# print(soup.find_all("title"))
# # [<title>The Dormouse's story</title>]
# print(soup.find_all("p", "title"))
# # [<p class="title"><b>The Dormouse's story</b></p>]
# print(soup.find_all("a"))
# # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
# #  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
# #  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
# print(soup.find_all(id="link2"))
# # [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
# import re
# print(soup.find(text=re.compile("sisters")))
# u'Once upon a time there were three little sisters; and their names were\n'

'''按CSS搜索
按照CSS类名搜索tag的功能非常实用,但标识CSS类名的关键字 class 在Python中是保留字,
使用 class 做参数会导致语法错误.从Beautiful Soup的4.1.1版本开始,
可以通过 class_ 参数搜索有指定CSS类名的tag
如果有多个class时可以完全匹配，也可以单个匹配
'''
# soup = BeautifulSoup(open("index2.html",encoding="utf-8"),features="lxml")
# #print(soup.find_all('p',class_='story'))
# print(soup.find_all("a", attrs={"class": "sister"})[0]['href'])
# print(soup.find_all("a", attrs={"class": "sister","id":"link2"})[0]['href'])

'''text参数
接受字符串 , 正则表达式 , 列表, True
'''
# soup_text=BeautifulSoup(open("index2.html",encoding='utf-8'),features='lxml')
# print(soup_text.find_all('a',text='Elsie'))
# print(soup_text.find_all('a',text=['Elsie',"Lacie"]))
# print(soup_text.find_all(text=['Elsie',"Lacie"]))#如果不指定标签，就是显示实际的文本

'''limit 参数
限制结果的数量
'''
# soup_text=BeautifulSoup(open("index2.html",encoding='utf-8'),features='lxml')
# print(soup_text.find_all("a"))#全部是三个
# print(soup_text.find_all("a",limit=2))#限制成两个

'''
记住: find_all() 和 find() 只搜索当前节点的所有子节点,孙子节点等. 
find_parents()-相当就是父节点和 find_parent()--相当就是父辈节点 用来搜索当前节点的父辈节点,搜索方法与普通tag的搜索方法相同,
搜索文档搜索文档包含的内容. 我们从一个文档中的一个叶子节点开始:
'''
# soup_text=BeautifulSoup(open("index2.html",encoding='utf-8'),features='lxml')
# text_parent=soup_text.find(text='Elsie')
# print(text_parent.find_parents('a'))#x相当--text_parent.find_parent()
# print(text_parent.find_parents('p',class_='storay'))#--父辈节点的P


'''find_next_siblings() 和 find_next_sibling()
find_next_siblings( name , attrs , recursive , text , **kwargs )
find_next_sibling( name , attrs , recursive , text , **kwargs )
find_previous_siblings() 和 find_previous_sibling()
'''
# soup_text=BeautifulSoup(open("index2.html",encoding='utf-8'),features='lxml')
# print(soup_text.a)
# frist_a=soup_text.find('a')
# print(frist_a.find_next_siblings())
# frist_b=soup_text.find('a',id='link2')
# print(frist_b.find_previous_sibling('a'))

'''6
CSS选择器¶,出来的结果都是list
'''
soup_text=BeautifulSoup(open("index2.html",encoding='utf-8'),features='lxml')
print(soup_text.select('title')[0].string)
#通过tag标签逐层查找:
#print(soup_text.select('body a'))
#找到某个tag标签下的直接子标签 [6] :
#print(soup_text.select('p > a'))
#找到兄弟节点标签:
# print(soup_text.select("#link1 ~.sister"))#只是往后的兄弟节点
# print(soup_text.select("#link3 ~.sister"))#只是往后的兄弟节点
# print(soup_text.select("#link1 + .sister"))
#通过CSS的类名查找:
# print(soup_text.select(".sister"))
# print(soup_text.select("[class~=sister]"))
#通过是否存在某个属性来查找:支持正则表达
print(soup_text.select("a[href]"))
