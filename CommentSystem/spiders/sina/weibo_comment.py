#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 23:08
# @Author  : qizai
# @File    : weibo_comment.py
# @Software: PyCharm

import re
import json
import copy
import datetime
import traceback
from scrapy import Request, Spider
from CommentSystem.items import CommentsItem


class SinaWeiBoSpider(Spider):
    name = "weibo_comment"
    allowed_domains = ["m.weibo.cn"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'CommentSystem.pipelines.MysqlPipeline': 301,
        }
    }

    comment_url = "https://m.weibo.cn/comments/hotflow?id={id}&mid={mid}&max_id_type={max_id_type}"  # max_id={max_id}&
    child_url = "https://m.weibo.cn/comments/hotFlowChild?cid={cid}&max_id={max_id}&max_id_type={max_id_type}"
    total = 0

    _id = "4505609644905372"
    mid = "4505609644905372"
    max_id_type = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; nxt-al10 Build/LYZ28N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 sinablog-android/5.3.2 (Android 5.1.1; zh_CN; huawei nxt-al10/nxt-al10)",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        # "Host": "passport.weibo.cn",
        "Origin": "https://passport.weibo.cn",
        "Accept": "*/*",
        "Connection": "keep-alive",

    }

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

        result = json.loads(response.text.replace("false", "0").replace("true", "1"))
        if result.get("ok")==1 and result.get("data").get("data"):
            comments = result.get("data").get("data")
            max_id = result.get("data").get("max_id")

            matcher = re.findall('(?<=XSRF-TOKEN=)[0-9a-zA-Z]{6,}(?=;)', str(response.headers).replace("XSRF-TOKEN=deleted", ""))
            headers = copy.deepcopy(self.headers)
            headers.update({
                "XSRF-TOKEN": matcher[0],
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Mode": "cors",
                "MWeibo-Pwa": "1",
                "Referer": "https://m.weibo.cn/detail/{}".format(self._id),
            })

            for comment in comments:
                comments_item = CommentsItem()
                field_map = {
                    # 'created_at': 'created_at',  # Sun May 17 16:38:17 +0800 2020
                    'comment_id': 'id',
                    'rootidstr': 'rootidstr',
                    'floor_number': 'floor_number',
                    'content': 'text',
                    'disable_reply': 'disable_reply',
                    'mid': 'mid',
                    'max_id': 'max_id',
                    'total_number': 'total_number',
                    'isAuthorLiked': 'isLikedByMblogAuthor',
                    'like_count': 'like_count',
                }
                for field, attr in field_map.items():
                    comments_item[field] = comment.get(attr)
                comments_item['created_at'] = self.format_time(comment.get("created_at"))
                comments_item['user_id'] = comment.get("user").get("id")
                comments_item['user_name'] = comment.get("user").get("screen_name")
                yield comments_item

                # 楼中楼,进一步爬取
                if comments_item["total_number"]>0:
                    yield Request(
                        url=self.child_url.format(cid=comments_item["comment_id"], max_id=0, max_id_type=0),
                        callback=self.parse_child,
                        headers=headers,
                        meta={"cid": copy.deepcopy(comments_item["comment_id"])}
                    )

            # if result.get("data").get("max_id_type")==0:
            print("1-继续请求下一页")
            yield Request(
                url=self.comment_url.format(id=self._id, max_id_type=result.get("data").get("max_id_type"), mid=self.mid)+"&max_id={}".format(result["data"]["max_id"]),
                callback=self.parse_comment,
                headers=headers,
                meta={"cid": copy.deepcopy(max_id)}
            )

    def parse_child(self, response):
        result = json.loads(response.text)
        if result.get("ok")==1 and result.get("data"):
            comments = result.get("data")
            max_id = result.get("max_id")
            max_id_type = result.get("max_id_type")
            for comment in comments:
                comments_item = CommentsItem()
                field_map = {
                    'comment_id': 'id',
                    'rootidstr': 'rootidstr',
                    'floor_number': 'floor_number',
                    'content': 'text',
                    'disable_reply': 'disable_reply',
                    'mid': 'mid',
                    'max_id': 'max_id',
                    'like_count': 'like_count',
                }
                for field, attr in field_map.items():
                    comments_item[field] = comment.get(attr)
                comments_item['created_at'] = self.format_time(comment.get("created_at"))
                comments_item['user_id'] = comment.get("user").get("id")
                comments_item['user_name'] = comment.get("user").get("screen_name")
                comments_item['max_id'] = max_id
                yield comments_item

            # 继续下一页
            print("2-child继续请求下一页")
            headers = copy.deepcopy(self.headers)
            matcher = re.findall('(?<=XSRF-TOKEN=)[0-9a-zA-Z]{6,}(?=;)', str(response.headers).replace("XSRF-TOKEN=deleted", ""))
            headers.update({
                "XSRF-TOKEN": matcher[0],
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Mode": "cors",
                "MWeibo-Pwa": "1",
                "Referer": "https://m.weibo.cn/detail/{}".format(self._id),
            })
            yield Request(
                url=self.child_url.format(cid=copy.deepcopy(response.meta["cid"]), max_id=max_id, max_id_type=max_id_type),
                callback=self.parse_child,
                headers=headers,
                meta={"cid": copy.deepcopy(max_id)}
            )
        pass

    @classmethod
    def format_time(cls, date_str):
        """
        处理评论时间
        :param date_str:
        :return:
        """
        GMT_FORMAT = "%a %b %d %H:%M:%S +0800 %Y"
        return datetime.datetime.strptime(date_str, GMT_FORMAT)




