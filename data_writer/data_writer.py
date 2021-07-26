#!/usr/bin/env python 3


import json
import time
import requests
from datetime import datetime


class ToutiaoDataWriter(object):
    """
    news data writer
    """

    def __init__(self):
        """
        初始化
        """
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt = time.strptime(time_now, "%Y-%m-%d %H:%M:%S")
        self.insert_time_stamp = int(time.mktime(dt))
        self.insert_time = time_now

    def do_write(self, datas: list):
        """
        :rtype: object
        """
        for data in datas:
            url = "http://localhost:8080"
            path = "/api/hotData/save"
            headers = {'content-type': "application/json"}
            body = {'title': data['title'],
                    'url': data['url'],
                    'content': data['content'],
                    'cnt': data['cnt'],
                    'siteName': data['site_name'],
                    'hotTag': data['hot_tag'],
                    'newsDailyNo': data['news_daily_no']
                    }
            rsp = requests.post(url + path, data=json.dumps(body), headers=headers)
        print("done")