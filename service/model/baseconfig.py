#!/usr/bin/env python3
'''
功能: 基本配置模型
'''

import json
from datetime import datetime
from common.const import *
from common.exception import RemoveException
from app import db

class Error(db.Model):
    '''错误信息对照'''
    __tablename__ = 'error'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    code = db.Column(db.Integer, unique=True)
    strcode = db.Column(db.CHAR(STRING_MEDIUM), unique=True, nullable=False)
    message = db.Column(db.String(STRING_MAX), nullable=False)

    def __init__(self, code=999, strcode='succ', message='Succeeded'):
        if code == 999:
            if Error.query.count() == 0:
                self.code = 1
            else:
                self.code = Error.query.filter(Error.code < 999) \
                                .order_by(Error.code.desc()).first().code + 1
        else:
            self.code = code
        self.strcode = strcode
        self.message = message


class Parameter(db.Model):
    '''系统运行参数'''
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    object = db.Column(db.CHAR(STRING_SMALL), nullable=False)
    attrib = db.Column(db.CHAR(STRING_MEDIUM), nullable=False)
    vtype = db.Column(db.String(STRING_SMALL), nullable=False, default='str')
    value = db.Column(db.String(STRING_MEDIUM), nullable=False)

    def __init__(self, obj, attr, val, vtype='str'):
        self.object = obj
        self.attrib = attr
        self.value = val
        self.vtype = vtype

    @classmethod
    def getlist(cls):
        return cls.query.all()

    @classmethod
    def getobj(cls, obj, attr=None):
        '''获取对象: 无属性时获取全部对象属性'''
        if attr == None:
            return cls.query.filter(cls.object == obj).all()
        return cls.query.filter( \
            cls.object == obj, cls.attrib == attr).first()

    @classmethod
    def getval(cls, obj, attr):
        '''获取值'''
        para = cls.query.filter( \
            cls.object == obj, cls.attrib == attr).first()
        if para == None:
            return None
        return eval(para.vtype)(para.value)

    @classmethod
    def setval(cls, obj, attr, val):
        '''设置值'''
        para = cls.query.filter( \
            cls.object == obj, cls.attrib == attr).first()

        if para == None:
            para = cls(obj, attr, str(val), type(val).__name__)
        else:
            para.value = str(val)
        db.session.add(para)

class UserLogModel(db.Model):
    ''' 用户日志 '''
    __tablename__ = 'user_log'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.CHAR(STRING_MEDIUM), nullable=False)
    ip = db.Column(db.CHAR(STRING_SMALL))
    source = db.Column(db.Integer)
    createtime = db.Column(db.DateTime, default=datetime.now)
    resourcename = db.Column(db.CHAR(STRING_MEDIUM))
    action = db.Column(db.INT)
    content = db.Column(db.CHAR(STRING_MAX))
    result = db.Column(db.CHAR(STRING_MEDIUM))

    def __init__(self, username, ip, source, createtime, resourcename, action, content, result):
        self.username = username;
        self.ip = ip
        self.source = source
        if createtime:
            self.createtime = createtime
        self.resourcename = resourcename
        self.action = action
        self.content = content
        self.result = result

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

