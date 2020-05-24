#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/16 12:16
# @Author  : qizai
# @File    : test.py
# @Software: PyCharm

import re
import requests

# url = "https://m.weibo.cn/comments/hotflow?id=4451505240900957&mid=4451505240900957&max_id_type=0"
# resp = requests.get(url)
# print(resp.text)
# print(resp.status_code)


headers = {'Server': ['Tengine/2.3.0'], 'Date': ['Sun, 17 May 2020 12:50:02 GMT'], 'Content-Type': ['application/json; charset=utf-8'], 'Vary': ['Accept-Encoding'], 'X-Powered-By': ['PHP/7.2.1'], 'Set-Cookie': ['XSRF-TOKEN=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/; domain=.weibo.cn', 'XSRF-TOKEN=13249a; expires=Sun, 17-May-2020 13:10:02 GMT; Max-Age=1200; path=/; domain=m.weibo.cn', 'MLOGIN=1; expires=Sun, 17-May-2020 13:50:02 GMT; Max-Age=3600; path=/; domain=.weibo.cn'], 'X-Log-Uid': ['2528335600'], 'Proc_Node': ['mweibo-172-16-42-150.tc.intra.weibo.cn'], 'Ssl_Node': ['ssl-008.mweibo.tc.intra.weibo.cn'], 'L': ['123.125.106.67'], 'Cache-Control': ['no-cache']}

matcher = re.findall('(?<=XSRF-TOKEN=)[0-9a-zA-Z]{6,}(?=;)', str(headers).replace("XSRF-TOKEN=deleted", ""))
print(matcher)


if __name__ == '__main__':
    pass


