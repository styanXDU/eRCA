# -*- coding: UTF-8 -*-
import requests
from lxml import etree

#请求头和目标网址
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}
url = 'https://bbs.sangfor.com.cn/plugin.php?id=case_databases:index&cpid=4'

#获取所有div标签
xpath_items = '//div[@id="threadList"]/div[@class="panel main-content"]'
# xpath_items = '//div[@class="panel main-content"]/div[@class="list-box_item clearfix posi-real ng-isolate-scope"]'
#对每个div标签再提取
xpath_link = './a/@href'
xpath_title= './div/h4/span/text()'
xpath_time = './div/div/ul/li/span/text()'

#获取和解析网页
r = requests.get(url, headers=headers)
r.encoding = r.apparent_encoding
dom = etree.HTML(r.text)

#获取所有的文章标签
items = dom.xpath(xpath_items)

#分别对每一个文章标签进行操作 将每篇文章的链接、标题和时间放到一个字典里
data = []
for article in items:
    t = {}
    t['link'] = article.xpath(xpath_link)[0]
    t['title'] = article.xpath(xpath_title)[0]
    t['time'] = article.xpath(xpath_time)[0]
    data.append(t)

#打印结果
for t in data:
    print(t)


