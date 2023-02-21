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

    #
    # def search_key_thesis(self, query, count: int = 10):
    #     ds1 = {
    #         "_source": {
    #             "includes": ["keywords"]
    #         },
    #         "query": {
    #             "multi_match": {
    #                 "query": query,
    #                 "fields": ["thesis_id"]
    #             }
    #         }
    #     }
    #     match_data = self.es.search(index=self.index_name, body=ds1, size=count)
    #     return match_data
    #
    # def search_thesis(self, query, count: int = 30):
    #     ds1 = {
    #         "_source": {
    #             "includes": ["thesis_id"]
    #         },
    #         "query": {
    #             "multi_match": {
    #                 "query": query,
    #                 "fields": ["keywords"]
    #             }
    #         }
    #     }
    #     match_data = self.es.search(index=self.index_name, body=ds1, size=count)
    #     return match_data
    #     关键词模糊查询
    def search(self, query: str, count: int = 20):
        ds1 = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["mingcheng^2", "weizhi"]
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=ds1, size=count)
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
