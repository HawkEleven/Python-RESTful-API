#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-09 10:54:16
# @Author  : Eleven (eleven.hawk@gmail.com)
# @Link    : https://github.com/HawkEleven
# @Version : 1.0

from urllib import request
from bs4 import BeautifulSoup

if __name__ == '__main__':
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
        print(href)
        print(imgUrl)
        print(title)
