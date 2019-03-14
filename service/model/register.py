import json
from app import db
from common.const import *
from common.const import STRING_MEDIUM





class RegisterModel(db.Model):
    '''注册码'''
    __tablename__ = 'register'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)#
    code = db.Column(db.CHAR(STRING_MEDIUM),nullable=False)#注册码
    Serial_id=db.Column(db.CHAR(STRING_SMALL), nullable=False)#产品序列号
    abbreviation=db.Column(db.CHAR(STRING_SMALL), nullable=False)#产品缩写

    def __init__(self,code,Serial_id,abbreviation):
        self.code = code
        self.Serial_id=Serial_id
        self.abbreviation=abbreviation

    @classmethod
    def deletecode(cls, code):
        '''清除注册码code'''
        cls.query.filter(cls.code == code).delete()

class SerialModel(db.Model):
    __tablename__ = 'serial_number'
    id = db.Column(db.Integer,autoincrement=True ,primary_key=True)  #id
    name = db.Column(db.CHAR(STRING_SMALL), nullable=False)
    abbreviation = db.Column(db.CHAR(STRING_SMALL), nullable=False)

    def __init__(self,name,abbreviation):
        self.name = name
        self.abbreviation = abbreviation
    @classmethod
    def getlist(cls):
        ''''''
        return cls.query.all()
