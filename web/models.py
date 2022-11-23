from extension import db
# 存储所有模型


class JiuFa(db.Model):
    __tablename__ = 'jiufa'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    mingcheng = db.Column(db.String(500), nullable=True)
    jieshao = db.Column(db.String(500), nullable=True)


class BingZheng(db.Model):
    __tablename__ = 'bingzheng'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    leibie = db.Column(db.String(500), nullable=True)
    bingming = db.Column(db.String(500), nullable=True)
    bingzheng = db.Column(db.String(500), nullable=True)
    zhiliao = db.Column(db.String(500), nullable=True)


class XueWei(db.Model):
    __tablename__ = 'xuewei'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    mingcheng = db.Column(db.String(500), nullable=True)
    weizhi = db.Column(db.String(500), nullable=True)
    gongxiao = db.Column(db.String(64000), nullable=True)
    zhuzhi = db.Column(db.String(64000), nullable=True)
    fangli = db.Column(db.String(64000), nullable=True)
    cijiufa = db.Column(db.String(64000), nullable=True)
    qita = db.Column(db.String(64000), nullable=True)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=True)
    mail = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(200), nullable=True)
