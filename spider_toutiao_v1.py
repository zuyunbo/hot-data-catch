#!/usr/bin/env python 3
# -*- coding: utf-8 -*-
"""
brief
Authors: zuyunbo
Date:    2021/07/21 16:24:00
"""
import json
import requests
import time
import sys
import hashlib
from datetime import datetime

from data_writer.data_writer import ToutiaoDataWriter


def str2value(valueStr):
    """
    å¼€å§‹spider
    """
    value = str(valueStr)
    idx_of_yi = value.find('亿')
    idx_of_wan = value.find('万')
    if idx_of_yi != -1 and idx_of_wan != -1:
        return int(float(valueStr[:idx_of_yi]) * 1e8 + float(valueStr[idx_of_yi + 1:idx_of_wan]) * 1e4)
    elif idx_of_yi != -1 and idx_of_wan == -1:
        return int(float(valueStr[:idx_of_yi]) * 1e8)
    elif idx_of_yi == -1 and idx_of_wan != -1:
        return int(float(valueStr[idx_of_yi + 1:idx_of_wan]) * 1e4)
    elif idx_of_yi == -1 and idx_of_wan == -1:
        return float(valueStr)


class SpiderV7(object):
    """
    spider
    """

    def __init__(self, baseurl):
        self.baseurl = baseurl
        self.data_list = []
        self.session = requests.session()
        self.headers = {
            "Connection": "close",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt = time.strptime(time_now, "%Y-%m-%d %H:%M:%S")
        self.insert_time_stamp = int(time.mktime(dt))
        self.insert_time = time_now

    def start_spider(self):
        """
        å¼€å§‹spider
        """
        res = self.session.get(url=self.baseurl, headers=self.headers)
        data = json.loads(res.text)

        result = []
        for tr in data['data']:

            if tr['Label'] == 'boom':
                hot_tag = '爆'
            elif tr['Label'] == 'hot':
                hot_tag = '热'
            else:
                hot_tag = ''

            data = {"content": '',
                    'title': tr['Title'],
                    'url': tr['Url'],
                    "cnt": tr['HotValue'],
                    'create_time_stamp': 0,
                    'hot_tag': hot_tag,
                    'site_name': ''
                    }
            result.append(data)
        for _, item in enumerate(result):
            # 生成ids
            m = hashlib.md5(item["title"].encode(encoding='utf-8'))
            item_id = m.hexdigest()
            item["news_daily_no"] = item_id
        return result

    def start(self):
        print('执行头条爬虫')
        baseurl = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'
        select_bre = SpiderV7(baseurl=baseurl)
        datalist = select_bre.start_spider()
        ToutiaoDataWriter().do_write(datalist)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        baseurl = sys.argv[1]
    else:
        baseurl = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'
    select_bre = SpiderV7(baseurl=baseurl)
    datalist = select_bre.start_spider()
    ToutiaoDataWriter().do_write(datalist)
