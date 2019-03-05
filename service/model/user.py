# !/usr/bin/env python3
'''
功能: 用户模型
'''

import json
from app import db
from common.const import *
from datetime import datetime

class UserModel(db.Model):
    ''' 用户 '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.CHAR(STRING_MEDIUM), nullable=False)
    password_hash = db.Column(db.CHAR(STRING_MEDIUM), nullable=False)
    email = db.Column(db.CHAR(STRING_MEDIUM), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    last_access_time = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=UserStatus.NORMAL)
    retry_login_count = db.Column(db.Integer, default=0)
    ip_set_text = db.Column(db.Text, default='')

    @property
    def ip_set(self):
        return json.loads(self.ip_set_text)

    @ip_set.setter
    def ip_set(self, ip_set):
        self.ip_set_text = json.dumps(ip_set, ensure_ascii=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = self._hash_password(password)

    def __init__(self, name, password, email, ip_set=None):
        self.name = name
        self.password = password
        self.email = email
        if not ip_set:
            self.ip_set = {
                'status': IpSetStatus.off,
                'rules':  []
            }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def verify_password(self, password):
        return self._hash_password(password) == self.password_hash

    def _hash_password(self, password):
        return password

    @classmethod
    def delete_by_id(cls, id):
        user = cls.query.filter(cls.id == id).first()
        if user:
            user.remove()

    def remove(self):
        logins = LoginModel.query.filter(LoginModel.userid == self.id).all()
        for login in logins:
            login.remove()
        db.session.delete(self)

    @classmethod
    def db_init(self):
        # 初始化数据

        user = UserModel('admin', '123456', '')
        db.session.add(user)


        user = UserModel('configadmin', '123456', '')
        db.session.add(user)

        user = UserModel('logadmin', '123456', '')
        db.session.add(user)


class LoginModel(db.Model):
    ''' 登录表 '''
    __tablename__ = 'login'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(STRING_MEDIUM))
    token = db.Column(db.String(STRING_MEDIUM), unique=True)
    sourcetype = db.Column(db.Integer, default=0)  # 来源 0.pc 1.移动
    createtime = db.Column(db.DateTime, default=datetime.now)
    lasttime = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def deletetoken(cls, token):
        '''清除登录token'''
        cls.query.filter(cls.token == token).delete()

    def remove(self):
        db.session.delete(self)
