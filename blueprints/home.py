from flask import (Blueprint, request)
from sqlalchemy import asc

from models import *
from util import Result
from es import ElasticSearch, create_es_data
from sqlalchemy.sql import func, literal_column

bp = Blueprint("home", __name__, url_prefix="/home")


# 查看Infor界面，第一次进入时需要去发送global信息
@bp.route("/InforView", methods=['GET'])
def find_Infor():
    data_id = int(request.args.get('id'))
    mode = int(request.args.get('category'))

    alldata_dict = []
    relation_dict = {
                        "jiufa": [],
                        "xuewei": [],
                        "bingzheng": [],
                    }
    if mode == 1:
        alldata = JiuFa.query.filter_by(id=data_id).first()
        jiufa_name = alldata.mingcheng
        query = Relation.query.filter_by(jiufa=jiufa_name).all()
        # 将结果组装成字典
        for row in query:
            xuewei = row.xuewei + " "
            bingzheng = row.bingzheng
            if xuewei not in [x[1] for x in relation_dict["xuewei"]]:
                main_infor = XueWei.query.filter_by(mingcheng=xuewei).first()
                if main_infor:
                    relation_dict["xuewei"].append([main_infor.id, main_infor.mingcheng])
            if bingzheng not in [x[1] for x in relation_dict["bingzheng"]]:
                main_infor = BingZheng.query.filter_by(mingcheng=bingzheng).first()
                relation_dict["bingzheng"].append([main_infor.id, main_infor.mingcheng])
    elif mode == 2:
        alldata = BingZheng.query.filter_by(id=data_id).first()
        # 查询 bingzheng 表获取 name
        bingzheng_name = alldata.mingcheng
        query = Relation.query.filter_by(bingzheng=bingzheng_name).all()
        # 将结果组装成字典
        for row in query:
            xuewei = row.xuewei + " "
            jiufa = row.jiufa
            if xuewei not in [x[1] for x in relation_dict["xuewei"]]:
                main_infor = XueWei.query.filter_by(mingcheng=xuewei).first()
                if main_infor:
                    relation_dict["xuewei"].append([main_infor.id, main_infor.mingcheng])
            if jiufa not in [x[1] for x in relation_dict["jiufa"]]:
                main_infor = JiuFa.query.filter_by(mingcheng=jiufa).first()
                relation_dict["jiufa"].append([main_infor.id, main_infor.mingcheng])
    else:
        alldata = XueWei.query.filter_by(id=data_id).first()
        xuewei_name = alldata.mingcheng.strip(" ")
        query = Relation.query.filter_by(xuewei=xuewei_name).all()
        # 将结果组装成字典
        for row in query:
            jiufa = row.jiufa
            bingzheng = row.bingzheng
            if jiufa not in [x[1] for x in relation_dict["jiufa"]]:
                main_infor = JiuFa.query.filter_by(mingcheng=jiufa).first()
                relation_dict["jiufa"].append([main_infor.id, main_infor.mingcheng])
            if bingzheng not in [x[1] for x in relation_dict["bingzheng"]]:
                main_infor = BingZheng.query.filter_by(mingcheng=bingzheng).first()
                relation_dict["bingzheng"].append([main_infor.id, main_infor.mingcheng])
    alldata_dict.append(alldata.to_dict())

    return Result.success_infor(alldata_dict, relation_dict)


@bp.route("/HomeView", methods=['GET'])
def home_load():
    # get请求，返回对应的所有条目
    if request.method == 'GET':
        mode = int(request.args.get('mode'))
        menuReady = request.args.get('menuReady')
        alldata_dict = []
        if mode == 1:
            alldata = JiuFa.query.all()
        elif mode == 2:
            alldata = BingZheng.query.all()
        else:
            alldata = XueWei.query.all()
        for single_data in alldata:
            alldata_dict.append({"id": single_data.id,
                                 "mingcheng": single_data.mingcheng})
        if menuReady == "false":
            menuList = {
                "灸法": {},
                "穴位": {},
                "病症": {},
            }
            # 灸法
            result = JiuFa.query.with_entities(JiuFa.leibie).group_by("leibie").all()
            for item in result:
                menuList["灸法"].update({item.leibie: []})
            result = JiuFa.query.all()
            for item in result:
                menuList["灸法"][item.leibie].append([item.id, 1, item.mingcheng])
            menuList["灸法"] = list(menuList["灸法"].items())

            # 病症

            result = BingZheng.query.with_entities(BingZheng.leibie).group_by(BingZheng.leibie).all()
            for item in result:
                menuList["病症"].update({item.leibie: []})
            result = BingZheng.query.order_by(func.CONVERT(literal_column('mingcheng using gbk'))).all()
            for item in result:
                menuList["病症"][item.leibie].append([item.id, 2, item.mingcheng])
            menuList["病症"] = list(menuList["病症"].items())
            # 穴位
            result = XueWei.query.with_entities(XueWei.leibie).group_by("leibie").all()
            for item in result:
                menuList["穴位"].update({item.leibie: []})
            result = XueWei.query.all()
            for item in result:
                menuList["穴位"][item.leibie].append([item.id, 3, item.mingcheng])
            menuList["穴位"] = list(menuList["穴位"].items())
            return Result.success_menu(alldata_dict, menuList)
        return Result.success(alldata_dict)

    # post请求，用于处理用户收藏
    else:
        data = request.get_json()
        if not data:
            return Result.error(400, 'post 必须是json数据')
        simple_id = data.get('id', None)
        category = data.get('category', None)
        user_name = data.get('user_name', None)
        if user_name == -1:
            message = "用户未登录"
            return Result.error(400, message)

        user_id = User.query.filter_by(user_name=user_name).first().user_id

        has_contain = Favorites.query.filter_by(data_id=simple_id, category=category, user_id=user_id).first()

        if has_contain:
            message = "该条目已收藏"
            return Result.error(400, message)

        favor = Favorites(data_id=simple_id, category=category, user_id=user_id)
        db.session.add(favor)
        db.session.commit()
        return Result.success("OK")


'''
    搜索功能
    1.目前：根据穴位的名称/位置进行一个简单匹配
    2.前端做了简单的分页，后端需要返回一个封装好的（1.总数 2.名称和位置）
    3.后续考虑加入筛选功能以及模糊匹配(2023.2.28 已完成)
'''


@bp.route("/search", methods=['POST'])
def search_words():
    # 参数设置，依次为：关键词，目前页数，单页条数，筛选条件，阈值，最大返回条数
    search_word = str(request.json.get('word'))
    search_page = int(request.json.get('page_number')) - 1
    page_size = int(request.json.get('page_size'))
    search_infor = list(request.json.get('select_infor').values())
    min_score = 1.0
    max_count = 100

    all_indexes = ["xuewei_infor", "jiufa_infor", "bingzheng_infor"]
    search_indexes = []

    for i in range(0, 3):
        if search_infor[i]:
            search_indexes.append(all_indexes[i])

    es = ElasticSearch(index_name=search_indexes)
    data = es.search(search_word, min_score, max_count)

    address_data = data["hits"]["hits"]
    data_number = len(address_data)
    # 取分页结果
    page_data = address_data[search_page*page_size:search_page*page_size + page_size]
    address_list = []
    for item in page_data:
        # 索引传递
        item["_source"]["index"] = item["_index"]
        address_list.append(item["_source"])
    return Result.success_search(address_list, data_number)


@bp.route("/createES")
def search_test():
    try:
        create_es_data()
        return "create OK"
    except Exception as e:
        return "Error" + str(e)
