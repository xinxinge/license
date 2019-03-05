#!/usr/bin/env python3
'''
功能: 系统运行参数
'''

from flask_restful import Resource, marshal_with

from flask_restful import Resource, marshal_with

from common.common import *
from common.const import *
from common.route import *
from common.utils import *
from model.baseconfig import Parameter
from app import db

class NoneClass():
    '''用于变量存储'''

    def __init__(self):
        pass

    def __repr__(self):
        '''输出参数'''
        replist = []
        objlist = self.__dict__.keys()
        for objstr in objlist:
            obj = getattr(self, objstr)
            attrlist = obj.__dict__.keys()
            for attr in attrlist:
                repstr = '%s.%s=[%s]' % (objstr, attr, str(getattr(obj, attr)))
                replist.append(repstr)

        return '\n'.join(replist)

para_fields = {
    'object': fields.String(attribute='object'),
    'attrib': fields.String(attribute='attrib'),
    'value':  fields.Raw(attribute='value'),
}

class Sysconfig(Resource):
    resourcename = 'Sysconfig'
    '''系统运行参数'''

    @classmethod
    def get_default(cls):
        syscfg = NoneClass()
        paralist = Parameter.getlist()
        for para in paralist:
            if not hasattr(syscfg, para.object):
                setattr(syscfg, para.object, NoneClass())
            attr = getattr(syscfg, para.object)
            setattr(attr, para.attrib, eval(para.vtype)(para.value))
        return syscfg

    @classmethod
    def set_default(cls):
        '''设置系统运行的默认配置'''
        # 只保留成功消息
        Error.query.delete()
        succ = Error(code=0, strcode='succ', message='Succeeded')
        db.session.add(succ)

        Parameter.query.delete()
        ############## 系统配置
        # URL前缀
        Parameter.setval('system', 'urlprefix', DEFURL)
        # 系统默认编码规则
        Parameter.setval('system', 'serialrule', ["$EQUIP_CATEGORY", "__", "$SERVICE", "__", "#"])
        # 安全设置(时间统一使用s)
        Parameter.setval('security', 'login_valid_time', 14400)
        Parameter.setval('security', 'login_free_time', 600)
        Parameter.setval('security', 'retry_login_count', 5)
        Parameter.setval('security', 'retry_login_type', RetryLoginType.no_pre_login)
        db_write()

    @response_marshal
    def get(self, obj, attr):
        '''获取系统参数'''

        if attr == 'all':
            para = Parameter.getobj(obj)
        else:
            para = Parameter.getobj(obj, attr)
        return send_data(para, para_fields)



class SyscfigList(Resource):
    resourcename = 'SyscfigList'

    @response_marshal
    @verify_token
    def get(self):
        '''获取可配置系统参数'''

        paralist = Parameter.getlist()

        return send_data(paralist, para_fields)

    @response_marshal
    @verify_token
    def put(self):
        '''设置系统参数'''

        try:
            arglist = self.jsondata
            for arg in arglist:
                Parameter.setval(arg.object, arg.attrib, arg.value)

            db_write()
        except Exception  as ex:
            return send_msg('argfmt', str(ex))

        return send_msg('succ')

ROUTES.add('sysconfig', Sysconfig, DEFURL + 'sysconfig/<string:obj>/<string:attr>', ['GET'])
ROUTES.add('sysconfiglist', SyscfigList, DEFURL + 'sysconfigs', ['GET', 'PUT'])
