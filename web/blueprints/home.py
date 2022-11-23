from flask import (Blueprint, render_template, request,
                   url_for)
from werkzeug.utils import redirect
from models import *

bp = Blueprint("home", __name__, url_prefix="/home")


# 工作台
@bp.route("/main")
def workspace():
    xuewei_tags = XueWei.query.all()
    bingzheng_tags = BingZheng.query.all()
    jiufa_tags = JiuFa.query.all()
    return render_template("mainHome.html", xueweiTags=xuewei_tags, bingzhengTags=bingzheng_tags, jiufaTags=jiufa_tags)


@bp.route("/xuewei")
def xuewei_load():
    index_id = request.args.get("index", True)
    xuewei_tag = XueWei.query.filter_by(id=index_id).first()
    return render_template("xueweiShow.html", tag=xuewei_tag)


@bp.route("/bingzheng")
def bingzheng_load():
    index_id = request.args.get("index", True)
    xuewei_tag = XueWei.query.filter_by(id=index_id).first()
    return render_template("xueweiShow.html", tag=xuewei_tag)


@bp.route("/search", methods=['GET', 'POST'])
def search_words():
    # 准确匹配查找
    if request.method == "GET":
        return render_template("searchPage.html")
    else:
        search_word = request.form.get("search_word")
        answers = XueWei.query.filter(XueWei.fangli.like("%" + search_word + "%")
                                      if search_word is not None else "").all()
        if search_word == "":
            answers = XueWei.query.all()

        return render_template("searchPage.html", answers=answers, word=search_word)






