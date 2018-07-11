#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-06 14:58:43
# @Author  : Eleven (eleven.hawk@gmail.com)
# @Link    : https://github.com/HawkEleven
# @Version : 1.0
# 爬虫数据

from bs4 import BeautifulSoup
from urllib import request
import chardet

from pymysql01 import MySQLCommand
from pymysql01 import SqlalchemyCommand

target_url = 'https://www.huxiu.com'
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
target_req = request.Request(url=target_url, headers=head)
target_response = request.urlopen(target_req)
target_html = target_response.read().decode('utf-8','ignore')

hot_article_soup = BeautifulSoup(target_html, 'lxml')
chapters = hot_article_soup.find_all('div', class_='box-moder hot-article hp-hot-article')
download_soup = BeautifulSoup(str(chapters), 'lxml')
hot_list = download_soup.select('.hot-article-img')

# 连接数据库
mysqlCommand = SqlalchemyCommand()
mysqlCommand.connectMysql()
dataCount = int(mysqlCommand.getLastId())
print('数据库数据个数', dataCount)

for new in hot_list:
    a = new.select('a')
    # 文章链接
    try:
        href = target_url + a[0]['href']
    except Exception:
        href = ''
    # 文章图片url
    try:
        imgUrl = a[0].select('img')[0]['src']
    except Exception as e:
        imgUrl = ''
    # 新闻标题
    try:
        title = a[0]['title']
    except Exception as e:
        title = ''

    #把爬取到的每条数据组合成一个字典用于数据库数据的插入
    news_dict = {
        "id": dataCount + 1,
        "title": title,
        "url": href,
        "img_path": imgUrl
    }
    print('----第%s条数据----' % (dataCount + 1))

    try:
        # 插入数据，如果已经存在就不再重复插入
        res = mysqlCommand.insertData(news_dict)
        if res:
            dataCount = res
            print('dataCount = ', dataCount)

    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句


mysqlCommand.closeMysql()  # 最后一定要要把数据关闭
dataCount = 0

    

