# -*- coding:utf-8 -*-
# @Author: IEeya

"""
    此文件主要用于提取主要的穴位/灸法名称，将其作为关键词对病症的bingzheng zhiliao两个属性进行广搜，从而建立相关联系。
    目标1：找到其中的所有相关
    目标2：根据nlp分析建立明确的关联模式（例如 感冒 艾条灸 大椎）
"""
import io
import sys

import numpy as np
import pandas as pd
import re

import xlwt as xlwt

xuewei_key_list = []
jiufa_key_list = []
path = "static/datas/艾灸.xls"
xuewei_path = "static/datas/病症穴位.xls"


# 保存到文件中
def saveData(savepath, datalist):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet('穴位病症', cell_overwrite_ok=True)
    col = ("start", "relation", "to")
    for i in range(0, 3):
        worksheet.write(0, i, col[i])
    i = 0
    for data in datalist:
        i = i+1
        for j in range(0, 3):
            try:
                worksheet.write(i, j, data[j])
            except IndexError:
                continue
    workbook.save(savepath)
    return 0


# 从穴位表中提取所有穴位词
def collect_key_words():
    xuewei_data = pd.read_excel(path, sheet_name="穴位", header=0, usecols=[0])
    jiufa_data = pd.read_excel(path, sheet_name="灸法", header=0, usecols=[0])
    xuewei_array = np.array(xuewei_data)
    jiufa_array = np.array(jiufa_data)
    for item in xuewei_array:
        xuewei_key_list.append(item[0].replace(" ", ""))
    for item in jiufa_array:
        jiufa_key_list.append(item[0].replace(" ", ""))


# 匹配穴位表与病症表的关系
def relation_xuewei():
    relation_result = []
    bingzheng_data = pd.read_excel(path, sheet_name="病症", header=0, usecols=[2, 3, 4])
    bingzheng_array = np.array(bingzheng_data)
    # 0:bingzheng, 1:zhiliao
    for item in bingzheng_array:
        # 方便正则提取
        item[2] = "。" + item[2]
        item_cut = re.split(r"。(.{0,20}?)\(一\)", item[2])
        # 去除开头
        del item_cut[0]
        if len(item_cut) % 2 != 0:
            print("size error !")
        # 组装
        element_from = ""
        relation_name = ""
        flag = True
        for element in item_cut:
            # 装填病症名和关系名
            if flag:
                element = re.sub(".*?。", "", element)
                element_from = item[0]
                relation_name = element
            # 提取穴位，这个算法很慢
            else:
                for key in xuewei_key_list:
                    if element.count(key):
                        relation_result.append([element_from, relation_name, key])
            flag = not flag
    saveData(xuewei_path, relation_result)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    collect_key_words()
    relation_xuewei()
