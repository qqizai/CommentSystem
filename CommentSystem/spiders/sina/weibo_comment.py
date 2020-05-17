#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 23:08
# @Author  : qizai
# @File    : weibo_comment.py
# @Software: PyCharm

import re
import json
import copy
import traceback
from scrapy import Request, Spider


class SinaWeiBoSpider(Spider):
    name = "weibo_comment"

    allowed_domains = ["m.weibo.cn"]
    comment_url = "https://m.weibo.cn/comments/hotflow?id={id}&mid={mid}&max_id_type={max_id_type}"  # max_id={max_id}&
    total = 0

    _id = "4505609644905372"
    mid = "4505609644905372"
    max_id_type = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; nxt-al10 Build/LYZ28N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 sinablog-android/5.3.2 (Android 5.1.1; zh_CN; huawei nxt-al10/nxt-al10)",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
    }

    cookies = {
        'XSRF-TOKEN': '7df30a',
        'MLOGIN': '1',
        # 'M_WEIBOCN_PARAMS': 'uicode%3D20000174',
        'WEIBOCN_FROM': '1110006030',  # 1110006030  1110005030
        '_T_WM': '48384861342',
        'SUB': "_2A25zxXz6DeRhGeRL6VoS8yvKyzyIHXVRRgSyrDV6PUJbktANLUL-kW1NU1Zt8kioG9zhfjrM4HrtaOujCt0u1jXO",
        'SUBP': "0033WrSXqPxfM725Ws9jqgMF55529P9D9WWofOfe78QiPRCZNab0b.pw5JpX5K-hUgL.Fozfeon0e0-ceh52dJLoIpjLxK.L1-BLBoeLxK-L1hMLBK2LxK.LBK5L1h-t",
        'SUHB': "0cS26eqICtNZxs",
    }

    # https://m.weibo.cn/comments/hotflow?id=4505609644905372&mid=4505609644905372&max_id=142554445903260&max_id_type=0
    # https://m.weibo.cn/comments/hotflow?id=4503524602083108&mid=4451505240900957&max_id_type=0&max_id=691344884916348

    # https://m.weibo.cn/comments/hotflow?id=4451505240900957&mid=4451505240900957&max_id_type=0
    # https://m.weibo.cn/comments/hotflow?max_id=153274557041735&id=4503524602083108&mid=4503524602083108&max_id_type=0
    def start_requests(self):
        # todo 需要从某个地方接任务，然后开始爬取( 可以是消息队列/数据库 )
        print("这里我来过了呀")
        yield Request(
            url=self.comment_url.format(id=self._id, max_id_type=self.max_id_type, mid=self.mid),
            callback=self.parse_comment,
            headers=self.headers,
        )

    def parse_comment(self, response):
        # TODO 进行解析全部的评论，有下一页继续调用自己进行解析
        # if isinstance(response.json)
        self.total += 1
        print("total:{} text: {}".format(self.total, response.text))

        matcher = re.findall('(?<=XSRF-TOKEN=)[0-9a-zA-Z]{6,}(?=;)', str(response.headers).replace("XSRF-TOKEN=deleted", ""))
        print(matcher)
        print(self.cookies)
        self.cookies.update({"XSRF-TOKEN": matcher[0]})
        print(self.cookies)
        headers = copy.deepcopy(self.headers)
        headers.update({
            "XSRF-TOKEN": matcher[0],
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Mode": "cors",
            "MWeibo-Pwa": "1",
            "Referer": "https://m.weibo.cn/detail/{}".format(self._id),
            "cookie": "_T_WM=48384861342; WEIBOCN_FROM=1110006030; ALF=1592313481; SCF=AmRuUbcLQzW9Si9aNynUXiFYzap67krRIqkXSrRbMZSG5PwROMLt68V1gAKpwAKqCpffBigpy8hk8RHOJ_P1MlM.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWofOfe78QiPRCZNab0b.pw5JpX5K-hUgL.Fozfeon0e0-ceh52dJLoIpjLxK.L1-BLBoeLxK-L1hMLBK2LxK.LBK5L1h-t; SUB=_2A25zxUs4DeRhGeRL6VoS8yvKyzyIHXVRRlVwrDV6PUJbkdAKLVXmkW1NU1Zt8gDwLA1Y0mwyIMoLqK2RSymlAjd3; SUHB=0xnTPJO1xuB0qd; SSOLoginState=1589721960; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4505609644905372%26luicode%3D10000011%26lfid%3D100103type%253D1%2526t%253D10%2526q%253D%25E5%2591%25A8%25E6%2589%25AC%25E9%259D%2592%2BP%25E7%2585%25A7%25E7%2589%2587%25E6%2598%25AF%25E7%25BD%2591%25E7%25BA%25A2%25E7%259A%2584%25E5%259F%25BA%25E6%259C%25AC%25E8%2581%258C%25E4%25B8%259A%25E7%25B4%25A0%25E5%2585%25BB%26uicode%3D20000061%26fid%3D4505609644905372; XSRF-TOKEN=c4c9d6",
        })

        try:
            datas = json.loads(response.text)
        except Exception as e:
            print(traceback.format_exc())
            datas = None
        if datas and datas["ok"]==1:
            print(self.comment_url.format(id=self._id, max_id_type=self.max_id_type, mid=self.mid)+"&max_id={}".format(datas["data"]["max_id"]))
            yield Request(
                url=self.comment_url.format(id=self._id, max_id_type=self.max_id_type, mid=self.mid)+"&max_id={}".format(datas["data"]["max_id"]),
                callback=self.parse_comment,
                headers=headers,
                cookies=self.cookies,
            )
        pass

    pass







