#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 23:08
# @Author  : qizai
# @File    : sina_weibo.py
# @Software: PyCharm

from scrapy import Request, Spider


class SinaWeiBoSpider(Spider):
    name = "sina_weibo"

    allowed_domains = ["m.weibo.cn"]

    # https://m.weibo.cn/comments/hotflow?max_id=153274557041735&id=4503524602083108&mid=4503524602083108&max_id_type=0
    def start_requests(self):
        pass

    def parse_comment(self):
        pass

    pass







