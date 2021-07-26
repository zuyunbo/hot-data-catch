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
from lxml import etree
from datetime import datetime


from data_writer.data_writer import ToutiaoDataWriter


class SpiderV5(object):
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
        html = etree.HTML(res.content)
        trs_list = html.xpath('//*[@id="listhot2"]/li/a')
        result = []
        for _, tr in enumerate(trs_list):
            tr_title = tr.xpath(".//text()")[0].strip()
            tr_url = tr.xpath(".//@href")[0].strip()

            data = {"content": '',
                    'title': tr_title,
                    'url': "https://tophub.today" + tr_url,
                    'create_time_stamp': 0,
                    'hot_tag': '',
                    'site_name': '',
                    'cnt': 0
                    }
            result.append(data)
        for _, item in enumerate(result):
            # 生成ids
            m = hashlib.md5(item["title"].encode(encoding='utf-8'))
            item_id = m.hexdigest()
            item["news_daily_no"] = item_id
        return result

    def start(self):
        print('执行澎湃爬虫')
        baseurl = 'https://www.thepaper.cn'
        select_bre = SpiderV5(baseurl=baseurl)
        datalist = select_bre.start_spider()
        ToutiaoDataWriter().do_write(datalist)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        baseurl = sys.argv[1]
    else:
        baseurl = 'https://www.thepaper.cn'
    select_bre = SpiderV5(baseurl=baseurl)
    datalist = select_bre.start_spider()
    ToutiaoDataWriter().do_write(datalist)
