from sqlalchemy import ForeignKey

from configs.extension import db
# 存储所有模型


class JiuFa(db.Model):
    __tablename__ = 'jiufa'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    leibie = db.Column(db.String(500), nullable=True)
    mingcheng = db.Column(db.String(500), nullable=True)
    jieshao = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        data = {
            'id': self.id,
            'leibie': self.leibie,
            'mingcheng': self.mingcheng,
            'jieshao': self.jieshao,
        }
        return data

    def to_search_dict(self):
        data = {
            'id': self.id,
            'mingcheng': self.mingcheng,
            'jieshao': self.jieshao,
        }
        return data


class BingZheng(db.Model):
    __tablename__ = 'bingzheng'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    leibie = db.Column(db.String(500), nullable=True)
    mingcheng = db.Column(db.String(500), nullable=True)
    bingzheng = db.Column(db.String(500), nullable=True)
    zhiliao = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        data = {
            'id': self.id,
            'leibie': self.leibie,
            'mingcheng': self.mingcheng,
            'bingzheng': self.bingzheng,
            'zhiliao': self.zhiliao,
        }
        return data

    def to_search_dict(self):
        data = {
            'id': self.id,
            'mingcheng': self.mingcheng,
            'bingzheng': self.bingzheng,
        }
        return data


class XueWei(db.Model):
    __tablename__ = 'xuewei'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    leibie = db.Column(db.String(500), nullable=True)
    mingcheng = db.Column(db.String(500), nullable=True)
    weizhi = db.Column(db.String(500), nullable=True)
    gongxiao = db.Column(db.String(64000), nullable=True)
    zhuzhi = db.Column(db.String(64000), nullable=True)
    fangli = db.Column(db.String(64000), nullable=True)
    cijiufa = db.Column(db.String(64000), nullable=True)
    qita = db.Column(db.String(64000), nullable=True)

    def to_search_dict(self):
        data = {
            'id': self.id,
            'mingcheng': self.mingcheng,
            'weizhi': self.weizhi,
        }
        return data

    def to_dict(self):
        data = {
            'id': self.id,
            'leibie': self.leibie,
            'mingcheng': self.mingcheng,
            'weizhi': self.weizhi,
            'gongxiao': self.gongxiao,
            'zhuzhi': self.zhuzhi,
            'fangli': self.fangli,
            'cijiufa': self.cijiufa,
            'qita': self.qita,
        }
        return data


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(30), nullable=True)
    motto = db.Column(db.String(150), nullable=True)

    def to_dict(self):
        """
        封装 User 对象，传递给前端只能是 json 格式，不能是实例对象
        :param include_email: 只有当用户请求自己数据时，才包含 email
        :return
        """
        data = {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'password': self.password,
            'email': self.email,
            'city': self.city,
            'motto': self.motto
        }
        return data

    def from_dict(self, data, new_user=False):
        """
        将前端发送过来的 json 对象转换为 User 对象
        :param data:
        :param new_user:
        :return:
        """

        for field in ['user_name', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.password = data['password']


class Likes(db.Model):
    __tablename__ = "likes"
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    infor_id = db.Column(db.Integer, nullable=False, primary_key=True)
    infor_category = db.Column(db.Integer, nullable=False, primary_key=True)


class Relation(db.Model):
    __tablename__ = "relation"
    __table_args__ = {'extend_existing': True}
    bingzheng = db.Column(db.String(20), nullable=False, primary_key=True)
    jiufa = db.Column(db.String(20), nullable=False, primary_key=True)
    xuewei = db.Column(db.String(20), nullable=False, primary_key=True)
