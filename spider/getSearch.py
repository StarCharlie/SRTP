# coding:utf-8

import os
import re  # 正则表达式提取文本
from jsonpath import jsonpath  # 解析json数据
import requests  # 发送请求
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用 作者：马哥python说 https://www.bilibili.com/read/cv17269127 出处：bilibili

url = 'https://m.weibo.cn/api/container/getIndex'
# 请求参数

params = {
    "containerid": "100103type=1&q={}".format("Warma"),
    "page_type": "searchall",
    "page": 1
}


def trans_time(v_str):
    """转换GMT时间为标准格式"""
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/99.0.4844.51 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }
    # 发送请求
    r = requests.get(url, headers=headers, params=params)
    print(r['data'])


if __name__ == "__main__":
    main()
