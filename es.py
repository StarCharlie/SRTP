# -*- coding:utf-8 -*-
# @Author: IEeya
from operator import or_

from elasticsearch import Elasticsearch
from sqlalchemy.orm import session, sessionmaker

from models import XueWei


class ElasticSearch:
    def __init__(self, index_name, index_type):
        self.es = Elasticsearch('http://localhost:9200')
        self.index_name = index_name
        self.index_type = index_type

    # 关键词模糊查询 + 分页机制
    # def search(self, query: str, page_number: int = 0, page_size: int = 10, max_size: int = 100):
    #     ds1 = {
    #         "min_score": 5.0,
    #         "query": {
    #             "multi_match": {
    #                 "query": query,
    #                 "fields": ["mingcheng^2", "weizhi"]
    #             }
    #         }
    #     }
    #     # 获取数据总量（期待有更好的解决办法）
    #     all_data_number = self.es.search(index=self.index_name, body=ds1, size=max_size)
    #     # 分页数据返回
    #     match_data = self.es.search(index=self.index_name, body=ds1, from_=page_number, size=page_size)
    #     return [match_data, len(all_data_number["hits"]["hits"])]

    # 简化版
    def search(self, query: str, max_size: int = 100):
        ds1 = {
            "min_score": 5.0,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["mingcheng^2", "weizhi"]
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=ds1, size=max_size)
        return match_data


def get_data():
    answers1 = XueWei.query.filter().all()
    alldata = []
    for single_thesis in answers1:
        single_data = XueWei.to_search_dict(single_thesis)
        alldata.append(single_data)
    return alldata


def create_es_data():
    es = Elasticsearch('http://localhost:9200')
    try:
        results = get_data()
        for row in results:
            infor = {
                "id": row['id'],
                "mingcheng": row['mingcheng'],
                "weizhi": row['weizhi']
            }
            es.index(index="xuewei_infor", document=infor)
        print("over")
    except Exception as e:
        print("Error:" + str(e))
