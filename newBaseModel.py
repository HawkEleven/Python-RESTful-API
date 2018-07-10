#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-06 17:57:54
# @Author  : Eleven (eleven.hawk@gmail.com)
# @Link    : https://github.com/HawkEleven
# @Version : 1.0

class NewBaseModel(object):
    """docstring for NewModel"""
    def __init__(self, id, title, img_path, url):
        self.id = id
        self.title = title
        self.img_path = img_path
        self.url = url

NewBaseModel('fjdk', 'fajk', 'wue', 'uei')
