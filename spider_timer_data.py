# !usr/bin/env python
# -*- coding:utf-8 _*-


# 导入线程模块
import threading
from spider_douyin_v1 import SpiderV4
from spider_pengpai_v1 import SpiderV5
from spider_suzhou_v1 import SpiderV6
from spider_toutiao_v1 import SpiderV7
from spider_xinlang_v1 import SpiderV8

def thread_Timer():
    print("执行爬虫")
    SpiderV4('123').start()
    SpiderV5('123').start()
    SpiderV6('123').start()
    SpiderV7('123').start()
    SpiderV8('123').start()


    # 声明全局变量
    global t1
    # 创建并初始化线程
    t1 = threading.Timer(50, thread_Timer)
    # 启动线程
    t1.start()


if __name__ == "__main__":
    # 创建并初始化线程
    t1 = threading.Timer(1, thread_Timer)
    # 启动线程
    t1.start()