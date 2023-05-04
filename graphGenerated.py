"""
    Author: IEeya syt 3200103483
    Date: 2023.2.9
    This file is used to generate a graph database based on neo4j (csv->neo4j)
    neo4j is deployed on port 7474 (localhost:7474)
"""
import numpy as np
import pandas as pd
import py2neo
from py2neo import Node, Relationship
from config import NEO4j_NAME, NEO4j_PASS, NEO4j_GRAPH

# database connection

graph = py2neo.Graph('neo4j://localhost:7687', auth=(NEO4j_NAME, NEO4j_PASS), name=NEO4j_GRAPH)
file_path = 'static/datas/艾灸.xls'

# relation_path = 'static/datas/病症穴位.xls'
relation_file_path = 'static/datas/关联表.xls'

max_count_test = 50


# 创建穴位单独节点以及类别关系
def create_xuewei_graph():
    xuewei_data = pd.read_excel(file_path, sheet_name="穴位", header=0)
    xuewei_array = np.array(xuewei_data)
    for i in range(0, len(xuewei_array)):
        node = Node('穴位',
                    id=xuewei_array[i][0],
                    name=xuewei_array[i][2].replace(" ", ""),
                    )
        relation = Node('类别',
                        name=xuewei_array[i][1])

        graph.create(node)
        graph.merge(relation, '类别', 'name')

        category_of_xuewei= Relationship(node, '属于', relation)
        graph.create(category_of_xuewei)
        graph.create(node)


# 创建灸法单独节点以及类别关系
def create_jiufa_graph():
    jiufa_data = pd.read_excel(file_path, sheet_name="灸法", header=0)
    jiufa_array = np.array(jiufa_data)
    for i in range(0, len(jiufa_array)):
        node = Node('灸法',
                    id=jiufa_array[i][0],
                    name=jiufa_array[i][2]
                    )
        relation = Node('类别',
                        name=jiufa_array[i][1])

        graph.create(node)
        graph.merge(relation, '类别', 'name')

        category_of_jiufa = Relationship(node, '属于', relation)
        graph.create(category_of_jiufa)


# create a new graph from scv
def create_bingzheng_graph():
    bingzheng_data = pd.read_excel(file_path, sheet_name="病症", header=0)
    bingzheng_array = np.array(bingzheng_data)
    # bingzheng_jiufa_xuewei_data = pd.read_excel(relation_file_path, sheet_name="Sheet1", header=0)
    # bingzheng_jiufa_xuewei_array = np.array(bingzheng_jiufa_xuewei_data)
    for i in range(0, len(bingzheng_array)):
        node = Node('病症',
                    id=bingzheng_array[i][0],
                    name=bingzheng_array[i][2])
        relation = Node('类别',
                        name=bingzheng_array[i][1])

        graph.create(node)
        graph.merge(relation, '类别', 'name')

        category_of_disease = Relationship(node, '属于', relation)
        graph.create(category_of_disease)

        # jiufa_nodes = []
        # for j in range(0, len(bingzheng_jiufa_xuewei_array)):
        #     if bingzheng_array[i][2] == bingzheng_jiufa_xuewei_array[j][0]:
        #         jiufa_name = bingzheng_jiufa_xuewei_array[j][1]
        #         jiufa_node = graph.nodes.match('灸法', name=jiufa_name).first()
        #
        #         if not jiufa_node:
        #             jiufa_node = Node('灸法', name=jiufa_name)
        #             jiufa_nodes.append(jiufa_node)
        #             graph.create(jiufa_node)
        #
        #         graph.merge(jiufa_node, '灸法', 'name')
        #         print(jiufa_node.values())
        #
        #         xuewei_nodes = []
        #         xuewei_name = bingzheng_jiufa_xuewei_array[j][2]  # assume xuewei node name is in the 4th column
        #         xuewei_node = graph.nodes.match('穴位', name=xuewei_name).first()
        #
        #         if not xuewei_node:
        #             xuewei_node = Node('穴位', name=xuewei_name)
        #             xuewei_nodes.append(xuewei_node)
        #             graph.create(xuewei_node)
        #
        #         graph.merge(xuewei_node, '穴位', 'name')
        #         print(xuewei_node.values())
        #         relation_name = '治疗' + bingzheng_array[i][2]
        #         jiufa_in_xuewei = Relationship(jiufa_node, relation_name, xuewei_node)
        #         graph.create(jiufa_in_xuewei)
        #
        #         jiufa_to_bingzheng = Relationship(node, '可用灸法', jiufa_node)
        #         # print(jiufa_to_bingzheng.values())
        #         graph.create(jiufa_to_bingzheng)


def create_disease_jiufa_xuewei_graph():
    disease_jiufa_xuewei_data = pd.read_excel(relation_file_path, sheet_name="Sheet1", header=0)
    disease_jiufa_xuewei_data_array = np.array(disease_jiufa_xuewei_data)
    for i in range(0, len(disease_jiufa_xuewei_data_array)):
        bingzheng_node = graph.nodes.match(name=disease_jiufa_xuewei_data_array[i][0]).first()
        jiufa_node = graph.nodes.match(name=disease_jiufa_xuewei_data_array[i][1]).first()
        xuewei_node = graph.nodes.match(name=disease_jiufa_xuewei_data_array[i][2]).first()
        # 病症灸法间关系
        relation = Relationship(bingzheng_node, "使用", jiufa_node)
        graph.create(relation)
        relation = Relationship(jiufa_node, "治疗", bingzheng_node)
        graph.create(relation)
        # 灸法穴位间关系
        relation = Relationship(jiufa_node, "针对", xuewei_node)
        graph.create(relation)
        # 病症穴位间关系
        relation = Relationship(bingzheng_node, "对应穴位", xuewei_node)
        graph.create(relation)
        relation = Relationship(xuewei_node, "关联", bingzheng_node)
        graph.create(relation)


def test():
    bingzheng_node = graph.nodes.match("病症", name='中风').first()
    print(dict(bingzheng_node))


# generated
if __name__ == '__main__':
    # delete all existing data
    graph.delete_all()
    # generating
    create_xuewei_graph()
    create_jiufa_graph()
    create_bingzheng_graph()
    create_disease_jiufa_xuewei_graph()
    print("create over")
