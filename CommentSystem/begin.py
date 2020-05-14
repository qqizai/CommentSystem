#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2020/5/14 10:17
# @Author   : qizai
# @File     : begin.py
# @Software : PyCharm

import os
import sys
import pathlib
import datetime


from scrapy.cmdline import execute


root_path = pathlib.Path(__file__).parent.parent
sys.path.append(root_path)

execute("scrapy crawl weibo_comment".split(" "))
