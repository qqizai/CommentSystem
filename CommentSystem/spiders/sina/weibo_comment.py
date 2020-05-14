#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 23:08
# @Author  : qizai
# @File    : weibo_comment.py
# @Software: PyCharm

from scrapy import Request, Spider


class SinaWeiBoSpider(Spider):
    name = "sina_weibo"

    allowed_domains = ["m.weibo.cn"]
    comment_url = "https://m.weibo.cn/comments/hotflow?max_id={max_id}&id={id}&mid={mid}&max_id_type={max_id_type}"
    total = 0

    # https://m.weibo.cn/comments/hotflow?max_id=153274557041735&id=4503524602083108&mid=4503524602083108&max_id_type=0
    def start_requests(self):
        # todo 需要从某个地方接任务，然后开始爬取( 可以是消息队列/数据库 )
        pass

    def parse_comment(self):
        # TODO 进行解析全部的评论，有下一页继续调用自己进行解析
        pass

    pass







