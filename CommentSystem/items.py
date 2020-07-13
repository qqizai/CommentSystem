# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class CommentsItem(Item):
    table = "comments"

    id = Field()
    weibo_url = Field()
    comment_id = Field()
    user_id = Field()
    user_name = Field()  # screen_name
    created_at = Field()
    rootidstr = Field()
    floor_number = Field()
    content = Field()
    disable_reply = Field()  # 是否关闭评论？
    mid = Field()
    max_id = Field()
    total_number = Field()  # 本条评论下有多少条回复
    isAuthorLiked = Field()  # 楼主是否点赞
    like_count = Field()
    crawled_at = Field()


class UserItem(Item):
    # collection是MongoDB的用法
    table = collection = 'users'
    # table是MySQL的用法
    # table = "users"  # 可用同时写：collection = table = 'users'

    id = Field()
    name = Field()
    avatar = Field()  # 头像
    cover = Field()
    gender = Field()
    description = Field()
    fans_count = Field()
    follows_count = Field()
    weibos_count = Field()
    verified = Field()
    verified_reason = Field()
    verified_type = Field()
    follows = Field()
    fans = Field()
    crawled_at = Field()


class UserRelationItem(Item):
    # collection = 'users'
    table = collection = 'user_relations'

    id = Field()
    follows = Field()
    fans = Field()


class WeiboItem(Item):
    table = collection = 'weibos'

    id = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    picture = Field()
    pictures = Field()
    source = Field()
    text = Field()
    raw_text = Field()
    thumbnail = Field()
    user = Field()
    created_at = Field()
    crawled_at = Field()






