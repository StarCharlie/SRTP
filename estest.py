from elasticsearch import Elasticsearch
from sqlalchemy import or_

from models import XueWei


class ElasticSearch:
    def __init__(self, index_name, index_type):
        self.es = Elasticsearch('http://localhost:9200')
        self.index_name = index_name
        self.index_type = index_type

    def search_key_thesis(self, query, count: int = 10):
        ds1 = {
            "_source": {
                "includes": ["keywords"]
            },
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["thesis_id"]
                }
            }
        }
        match_data = self.es.search(index=self.index_name, document=ds1, size=count)
        return match_data

    def search_thesis(self, query, count: int = 30):
        ds1 = {
            "_source": {
                "includes": ["thesis_id"]
            },
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["keywords"]
                }
            }
        }
        match_data = self.es.search(index=self.index_name, document=ds1, size=count)
        return match_data

    def search(self, query: str, count: int = 30):
        ds1 = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["mingcheng", "weizhi"]
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=ds1, size=count)
        return match_data


def get_data():
    query = XueWei.query.filter_by(XueWei.id, XueWei.mingcheng, XueWei.weizhi).all()
    print(query)
    return query


def create_es_data():
    es = Elasticsearch('http://localhost:9200')
    try:
        results = get_data()
        for row in results:
            infor = {
                "id": row[0],
                "mingcheng": row[1],
                "weizhi": row[2]
            }
            es.index(index="xuewei_infor", document=infor)
    except Exception as e:
        print("Error:" + str(e))


def main():
    get_data()
    es = ElasticSearch(index_name="xuewei_infor", index_type="test-type")
    data = es.search("涌泉")
    address_data = data["hits"]["hits"]
    address_list = []
    for item in address_data:
        address_list.append(item["_source"])
    print(address_list)


def get_data():
    search_word = "云"
    query = XueWei.query.filter(or_(XueWei.mingcheng.like("%" + search_word + "%"),
                                    XueWei.weizhi.like("%" + search_word + "%"))
                                if search_word is not None else "").limit(20).all()
    print(query)
    return query


def create_es_data():
    es = Elasticsearch('http://localhost:9200')
    try:
        results = get_data()
        for row in results:
            infor = {
                "id": row[0],
                "mingcheng": row[1],
                "weizhi": row[2]
            }
            result = es.index(index="xuewei_infor", document=infor)
            print(result)
    except Exception as e:
        print("Error:" + str(e))


def search(self, query: str, count: int = 30):
    ds1 = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["mingcheng", "weizhi"]
            }
        }
    }
    match_data = self.es.search(index=self.index_name, body=ds1, size=count)
    return match_data


if __name__ == '__main__':
    main()
