from flask import (Blueprint, request)
from sqlalchemy import or_

from models import *
from util import Result
from es import ElasticSearch, create_es_data

bp = Blueprint("home", __name__, url_prefix="/home")


# 工作台
@bp.route("/InforView", methods=['GET'])
def find_Infor():
    data_id = int(request.args.get('id'))
    mode = int(request.args.get('category'))
    alldata_dict = []
    if mode == 1:
        alldata = JiuFa.query.filter_by(id=data_id).first()
    elif mode == 2:
        alldata = BingZheng.query.filter_by(id=data_id).first()
    else:
        alldata = XueWei.query.filter_by(id=data_id).first()
    dic_tret = dict(alldata.__dict__)
    dic_tret.pop('_sa_instance_state', None)
    alldata_dict.append(dic_tret)
    return Result.success(alldata_dict)


@bp.route("/HomeView", methods=['GET'])
def home_load():
    # get请求，返回对应的所有条目
    if request.method == 'GET':
        mode = int(request.args.get('mode'))
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
    3.后续考虑加入筛选功能以及模糊匹配
'''


@bp.route("/search", methods=['POST'])
def search_words():
    search_word = request.json.get('word')
    answers1 = XueWei.query.filter(or_(XueWei.mingcheng.like("%" + search_word + "%"),
                                   XueWei.weizhi.like("%" + search_word + "%"))
                                   if search_word is not None else "").limit(20).all()
    alldata = []
    for single_thesis in answers1:
        single_data = XueWei.to_search_dict(single_thesis)
        alldata.append(single_data)

    key_word = search_word
    keyword = str(key_word)
    es = ElasticSearch(index_name="xuewei_infor", index_type="test-type")
    data = es.search(keyword)
    print(data)
    address_data = data["hits"]["hits"]
    address_list = []
    for item in address_data:
        address_list.append(item["_source"])
    print(address_list)

    return Result.success(address_list)
