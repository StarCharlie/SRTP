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
import pyodbc

# database connection

graph = py2neo.Graph('neo4j://localhost:7687', auth=(NEO4j_NAME, NEO4j_PASS), name=NEO4j_GRAPH)
file_path = 'static/datas/艾灸.xls'
relation_path = 'static/datas/病症穴位.xls'

file_path2 = 'static/datas/灸法.xls'

file_path3 = 'static/datas/外科皮肤科.xls'

max_count_test = 50


# create a new graph from scv
def create_bingzheng_graph():
    bingzheng_data = pd.read_excel(file_path, sheet_name="病症", header=0)
    bingzheng_array = np.array(bingzheng_data)

    bingzheng_jiufa_xuewei_data = pd.read_excel(file_path3, sheet_name="Sheet1", header=0)
    bingzheng_jiufa_xuewei_array = np.array(bingzheng_jiufa_xuewei_data)
    print(bingzheng_jiufa_xuewei_array)
    for i in range(0, len(bingzheng_array)):
        node = Node('disease',
                    id=bingzheng_array[i][0],
                    name=bingzheng_array[i][2],
                    bingzheng=bingzheng_array[i][3],
                    zhiliao=bingzheng_array[i][4])
        relation = Node('category',
                        name=bingzheng_array[i][1])

        graph.create(node)
        print(node.values())
        graph.merge(relation, 'category', 'name')

        category_of_disease = Relationship(node, '属于', relation)
        # print(relation.values())
        graph.create(category_of_disease)

        jiufa_nodes = []
        for j in range(0, len(bingzheng_jiufa_xuewei_array)):
            if(bingzheng_array[i][2] == bingzheng_jiufa_xuewei_array[j][0]):
                jiufa_name = bingzheng_jiufa_xuewei_array[j][1]
                jiufa_node = graph.nodes.match('jiufa', name=jiufa_name).first()

                if not jiufa_node:
                    jiufa_node = Node('jiufa', name=jiufa_name)
                    jiufa_nodes.append(jiufa_node)
                    graph.create(jiufa_node)

                graph.merge(jiufa_node, 'jiufa', 'name')
                print(jiufa_node.values())

                xuewei_nodes = []
                xuewei_name = bingzheng_jiufa_xuewei_array[j][2]  # assume xuewei node name is in the 4th column
                xuewei_node = graph.nodes.match('acupoint', name=xuewei_name).first()

                if not xuewei_node:
                    xuewei_node = Node('acupoint', name=xuewei_name)
                    xuewei_nodes.append(xuewei_node)
                    graph.create(xuewei_node)

                graph.merge(xuewei_node, 'acupoint', 'name')
                print(xuewei_node.values())
                relation_name = '治疗'+bingzheng_array[i][2]
                jiufa_in_xuewei = Relationship(jiufa_node, relation_name, xuewei_node)
                graph.create(jiufa_in_xuewei)


                jiufa_to_bingzheng = Relationship(node,'可用灸法', jiufa_node)
                # print(jiufa_to_bingzheng.values())
                graph.create(jiufa_to_bingzheng)


def create_xuewei_graph():
    xuewei_data = pd.read_excel(file_path, sheet_name="穴位", header=0)
    xuewei_array = np.array(xuewei_data)
    for i in range(0, len(xuewei_array)):
        node = Node('acupoint',
                    id=xuewei_array[i][0],
                    name=xuewei_array[i][1].replace(" ", ""),
                    position=xuewei_array[i][2],

                    )
        graph.create(node)


def create_disease_xuewei_relation():
    bingzheng_xuewei_data = pd.read_excel(relation_path, sheet_name="穴位病症", header=0)
    bingzheng_xuewei_array = np.array(bingzheng_xuewei_data)
    for i in range(0, len(bingzheng_xuewei_array)):
        if i == max_count_test:
            break
        bingzheng_node = graph.nodes.match(name=bingzheng_xuewei_array[i][0]).first()
        xuewei_node = graph.nodes.match(name=bingzheng_xuewei_array[i][2]).first()
        xuewei_of_bingzheng = Relationship(bingzheng_node, bingzheng_xuewei_array[i][1], xuewei_node)
        graph.create(xuewei_of_bingzheng)


def create_jiufa_graph():
    jiufa_data = pd.read_excel(file_path2, sheet_name="jiufa", header=0)
    jiufa_array = np.array(jiufa_data)
    for i in range(0, len(jiufa_array)):
        node = Node('jiufa',
                    id=jiufa_array[i][0],
                    name=jiufa_array[i][2]
                    )
        relation = Node('category',
                        name=jiufa_array[i][1])

        graph.create(node)
        graph.merge(relation, 'category', 'name')

        category_of_jiufa = Relationship(node, '包括', relation)
        graph.create(category_of_jiufa)

def create_disease_jiufa_xuewei_graph():
    disease_jiufa_xuewei_data = pd.read_excel(file_path3, sheet_name="Sheet1", header=0)
    print(disease_jiufa_xuewei_data)
    disease_jiufa_xuewei_data_array = np.array(disease_jiufa_xuewei_data)
    for i in range(0, len(disease_jiufa_xuewei_data_array)):
        node = Node('disease',
                    name=disease_jiufa_xuewei_data_array[i][0],
                    )
        relation1 = Node('jiufa',
                        name=disease_jiufa_xuewei_data_array[i][1])
        # relation2 = Node('xuewei',
        #                 name=disease_jiufa_xuewei_data_array[i][2])

        graph.create(node)
        graph.merge(relation1, 'jiufa', 'name')
        # graph.merge(relation2, 'xuewei', 'name')

        category_of_disease_jiufa_xuewei_data1 = Relationship(node, '治疗', relation1)
        # category_of_disease_jiufa_xuewei_data2 = Relationship(node, '治疗', relation2)
        graph.create(category_of_disease_jiufa_xuewei_data1)
        # graph.create(category_of_disease_jiufa_xuewei_data2)


def test():
    bingzheng_node = graph.nodes.match("disease", name='中风').first()
    print(dict(bingzheng_node))


# generated
if __name__ == '__main__':
    # delete all existing data
    graph.delete_all()
    # generating
    create_bingzheng_graph()
    create_xuewei_graph()
    create_disease_xuewei_relation()
    create_jiufa_graph()
    # create_disease_jiufa_xuewei_graph()
    print("create over")
