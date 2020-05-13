#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 23:08
# @Author  : qizai
# @File    : sina_weibo.py
# @Software: PyCharm

import scrapy


class SinaWeiBoSpider(scrapy.spiders):
    name = "sina_weibo"

    allowed_domains = ["m.weibo.cn"]

    def start_requests(self):
        pass
    pass







