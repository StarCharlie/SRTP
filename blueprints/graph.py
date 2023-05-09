# -*- coding:utf-8 -*-
# @Author: IEeya
from flask import (Blueprint, request)

from configs.models import *
from configs.util import Result

bp = Blueprint("graph", __name__, url_prefix="/graph")


@bp.route("/GetInfor", methods=['POST'])
def find_Infor():
    data = request.get_json()
    if not data:
        return Result.error(400, 'post 必须是json数据')
    name = data.get('name', None)
    category = data.get('category', None)
    if category == "灸法":
        category_id = 1
        result = JiuFa.query.filter_by(mingcheng=name).first()
    elif category == "病症":
        category_id = 2
        result = BingZheng.query.filter_by(mingcheng=name).first()
    else:
        category_id = 3
        result = XueWei.query.filter_by(mingcheng=name).first()
    if not result:
        return Result.error(404, "找不到对应数据")
    return Result.success({
        "id": result.id,
        "category": category_id
    })
