# -*- coding:utf-8 -*-
# @Author: IEeya


"""
    更新：2023.2.27
    利用ES搜索引擎来辅助文章的整体搜索：
    ElasticSearch类：包含index_name：索引表名称单属性。
    本程序中针对穴位、病症、灸法均有一张索引表，方便用户搜索
    api：
        Elasticsearch.search(str query, float min_score, int max_size)：输入查找符与阈值与返回上限，返回查找列表
        create_es_data()：初始化搜索库【注意，除非有必要修改，否则不要擅自调用这个函数
                        如果需要直接调用，可以通过访问localhost:5000/home/createES实现，出现create OK后说明调用成功】
"""


from elasticsearch import Elasticsearch
from configs.models import XueWei, BingZheng, JiuFa


class ElasticSearch:
    def __init__(self, index_name):
        self.es = Elasticsearch('http://localhost:9200')
        self.index_name = index_name

    # 简化版
    def search(self, query: str, min_score: float = 5.0, max_size: int = 100):
        ds1 = {
            "min_score": min_score,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "infor"]
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=ds1, size=max_size)
        return match_data


def get_xuewei_data():
    answers1 = XueWei.query.filter().all()
    alldata = []
    for single_thesis in answers1:
        single_data = XueWei.to_search_dict(single_thesis)
        alldata.append(single_data)
    return alldata


def get_jiufa_data():
    answers1 = JiuFa.query.filter().all()
    alldata = []
    for single_thesis in answers1:
        single_data = JiuFa.to_search_dict(single_thesis)
        alldata.append(single_data)
    return alldata


def get_bingzheng_data():
    answers1 = BingZheng.query.filter().all()
    alldata = []
    for single_thesis in answers1:
        single_data = BingZheng.to_search_dict(single_thesis)
        alldata.append(single_data)
    return alldata


# 注意，使用该函数前务必询问负责人【仅可通过/home/createES询问】
def create_es_data():
    es = Elasticsearch('http://localhost:9200')
    es.indices.delete(index="xuewei_infor")
    es.indices.delete(index="jiufa_infor")
    es.indices.delete(index="bingzheng_infor")

    try:
        # 为了方便多索引联合查询，尽量保证索引结构一致
        results = get_xuewei_data()
        for row in results:
            infor = {
                "id": row['id'],
                "title": row['mingcheng'],
                "infor": row['weizhi']
            }
            es.index(index="xuewei_infor", document=infor)

        results = get_jiufa_data()
        for row in results:
            infor = {
                "id": row['id'],
                "title": row['mingcheng'],
                "infor": row['jieshao']
            }
            es.index(index="jiufa_infor", document=infor)
        results = get_bingzheng_data()
        for row in results:
            infor = {
                "id": row['id'],
                "title": row['mingcheng'],
                "infor": row['bingzheng']
            }
            es.index(index="bingzheng_infor", document=infor)
        print("over")
    except Exception as e:
        print("Error:" + str(e))
