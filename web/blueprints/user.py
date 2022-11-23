from flask import (Blueprint, render_template, request,
                   url_for, flash)
from werkzeug.utils import redirect
from models import *

bp = Blueprint("user", __name__, url_prefix="/user")


# 主界面，用来存放登录与注册相关按钮
@bp.route("/")
def index():
    return redirect(url_for("user.workspace"))


# 工作台
@bp.route("/main")
def workspace():
    # 用户主界面
    # 后续用这句：return render_template("userHome.html")
    return redirect(url_for("home.workspace"))


@bp.route("/login", methods=['GET', 'POST'])
def user_login():
    if request.method == "GET":
        return render_template("userLogin.html")
    else:
        form = request.form
        user_name = form.get("user_name")
        user_password = form.get("user_password")
        check = User.query.filter_by(name=user_name).first()
        if check:
            check_password = (check.password == user_password)
            if check_password:
                return redirect(url_for("user.workspace"))
            else:
                flash("密码错误")
        else:
            flash("用户不存在")
        # 转到用户主界面
        return redirect(url_for("user.user_login"))


@bp.route("/register", methods=['GET', 'POST'])
def user_register():
    # 准确匹配查找
    if request.method == "GET":
        return render_template("userRegister.html")
    else:
        form = request.form
        user_name = form.get("user_name")
        user_mail = form.get("user_mail")
        user_password = form.get("user_password")
        check = User.query.filter_by(name=user_name).first()
        if check:
            flash("用户名重复")
            return redirect(url_for("user.user_register"))
        else:
            # 提交注册
            new_user = User(name=user_name, mail=user_mail, password=user_password)
            db.session.add(new_user)
            db.session.commit()
            # 转到用户登录界面
            return redirect(url_for("user.user_login"))






