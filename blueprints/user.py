# 用户界面
from flask import Blueprint, request
from models import *
from util import Result

bp = Blueprint("user", __name__, url_prefix="/user")


# POST:将前端的数据提交给服务器
@bp.route("LoginView", methods=["POST"])
def login_view():
    data = request.get_json()
    if not data:
        return Result.error(400, 'post 必须是json数据')
    username = data.get('username', None)
    password = data.get('password', None)
    query = User.query.filter_by(user_name=username).first()
    if not query:
        message = '该用户不存在!'
        return Result.error(400, message)
    else:
        if query.password == password:
            return Result.success("登陆成功!")
        else:
            message = '密码错误,登陆失败!'
            return Result.error(400, message)


@bp.route("RegisterView", methods=["POST", "GET"])
def register_view():
    data = request.get_json()
    if not data:
        return Result.error(400, 'post 必须是json数据')
    message = {}
    username = data.get('user_name', None)
    email = data.get('email', None)
    # 检查数据库中是否有该用户
    check1 = User.query.filter_by(user_name=username).first()
    check2 = User.query.filter_by(email=email).first()
    if check1:
        message = '用户名已存在'
    if check2:
        message = '邮箱已存在'
    if message:
        return Result.error(400, message)

    # 创建新用户
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return Result.success("OK")


@bp.route("UserView", methods=['GET', 'POST'])
def user_simple_data():
    if request.method == 'GET':
        name = request.args.get('user_name')
        user = User.query.filter_by(user_name=name).first()
        return Result.success(User.to_dict(user))
    else:
        data = request.get_json()
        if not data:
            return Result.error(400, 'post 必须是json数据')
        old_name = data.get('old_name', None)
        user_id = User.query.filter_by(user_name=old_name).first().user_id
        if not user_id:
            message = "用户不存在"
            return Result.error(400, message)
        new_name = data.get('new_name', None)
        city = data.get('city', None)
        motto = data.get('motto', None)
        email = data.get('email', None)
        user = User.query.filter_by(user_id=user_id).first()
        user.user_name = new_name
        user.city = city
        user.motto = motto
        user.email = email
        db.session.commit()
        return Result.success("OK")


@bp.route("UserPassword", methods=['GET', 'POST'])
def user_password_data():
    data = request.get_json()
    if not data:
        return Result.error(400, 'post 必须是json数据')
    name = data.get('name', None)
    password = data.get('pass', None)
    user = User.query.filter_by(user_name=name).first()
    if not user:
        message = "用户不存在"
        return Result.error(400, message)
    user.password = password
    db.session.commit()
    return Result.success("OK")
