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

max_count_test = 50


# create a new graph from scv
def create_bingzheng_graph():
    bingzheng_data = pd.read_excel(file_path, sheet_name="病症", header=0)
    bingzheng_array = np.array(bingzheng_data)
    for i in range(0, len(bingzheng_array)):
        node = Node('disease',
                    id=bingzheng_array[i][0],
                    name=bingzheng_array[i][2],
                    bingzheng=bingzheng_array[i][3],
                    zhiliao=bingzheng_array[i][4])
        relation = Node('category',
                        name=bingzheng_array[i][1])

        graph.create(node)
        graph.merge(relation, 'category', 'name')

        category_of_disease = Relationship(node, '属于', relation)
        print(relation.values())
        graph.create(category_of_disease)


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
    print("create over")
