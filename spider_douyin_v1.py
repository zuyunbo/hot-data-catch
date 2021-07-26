#!/usr/bin/env python 3
# -*- coding: utf-8 -*-
"""
brief
Authors: zuyunbo
Date:    2021/07/21 16:24:00
"""
import requests
import time
import hashlib
from lxml import etree
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


class SpiderV4(object):
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

        path = u'//*[@class="jc-c"]/table/tbody/tr'

        trs_list = html.xpath(path)
        result = []
        for _, tr in enumerate(trs_list):
            tr_title = tr.xpath(".//td[contains(@class, 'al')]/a/text()")[0].strip()
            tr_nums = tr.xpath(".//td[last()-1]/text()")[0].strip()
            tr_url = tr.xpath(".//td[contains(@class, 'al')]/a/@href")[0].strip()

            data = {"content": '',
                    'title': tr_title,
                    'url': "https://tophub.today" + tr_url,
                    "cnt": str2value(tr_nums),
                    'create_time_stamp': 0,
                    'hot_tag': '',
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
        print('执行抖音爬虫')
        baseurl = 'https://tophub.today/n/K7GdaMgdQy'
        select_bre = SpiderV4(baseurl=baseurl)
        datalist = select_bre.start_spider()
        ToutiaoDataWriter().do_write(datalist)


if __name__ == "__main__":
   print('1')