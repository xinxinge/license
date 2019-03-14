import uuid
import datetime

from common.algorithm import License, LIC_ONTRIAL
from common.common import *
from common.route import ROUTES
from common.utils import paging
from flask_restful import Resource, fields
from model.register import *


arv_fields = {
    'name':              fields.String,
    'abbreviation':      fields.String,
}
class Register_code(Resource):
    #生成注册码
    resourcename = 'Register_code'
    @response_marshal
    @verify_token(loginflag=0)
    def post(self, ):
        '''生成注册码'''
        args=self.jsondata
        lic=License()
        lic.setLicType(0)#状态
        lic.setCustomer('机柜')#客户名称
        lic.setMaxCabinet(50)#独有属性如有机柜数
        lic.setProductid('DC00000001')#序列号
        lic.setValidation(60)#有效期
        lic.encrypt_keystr()
        msg=lic.getInfo()
        # msg= uuid.uuid3(uuid.NAMESPACE_DNS,args.name)#根据序列号生成注册码 v
        if not msg:
            return send_msg('fail', '注册码获取失败')

        create_time=datetime.datetime.now()#获取系统当前时间
        delta=datetime.timedelta(days=args.day)
        last_access_time = (create_time + delta).strftime("%Y--%m--%d %H:%M:%S")
        #计算有效时间
        newuser = RegisterModel( str(msg), args.product_id,args.aabbreviation)
        db.session.add(newuser)
        dbflag, dbmsg = db_write()
        if dbflag:
            return send_msg('dberror', dbmsg)
        return send_msg('succ', str(msg))


class Serial_number(Resource):
    resourcename = 'Serial_number'
    @response_marshal
    @verify_token(loginflag=0)
    def post(self):
        ars=self.json
        num= RegisterModel.query.filter(RegisterModel.abbreviation==ars.abbreviation).all
        if not num:
            index = 1
        else:
            index = len(num)
        nums = 10 - len(ars.name +ars.test+ str(index))
        msg=ars.name + ars.test + '0'*nums+ str(index)
        return send_msg('succ', msg)


class Product_list(Resource):
    '''产品列表'''
    resourcename = 'Product_list'
    @response_marshal
    @verify_token(loginflag=0)
    def get(self):
        data = SerialModel.getlist()
        return send_data(data, arv_fields)

    @response_marshal
    @verify_token(loginflag=0)
    def post(self):
        ars=self.json
        newuser = SerialModel(ars.name,ars.abbreviation)
        db.session.add(newuser)
        dbflag, dbmsg = db_write()
        if dbflag:
            return send_msg('dberror', dbmsg)
        return send_msg('succ', '添加成功')

ROUTES.add('Register_code', Register_code, DEFURL + 'Register_code', [ 'GET','POST'])
ROUTES.add('Product_list', Product_list, DEFURL + 'Product_list', ['GET','POST'])
ROUTES.add('Serial_number', Serial_number, DEFURL + 'Serial_number', [ 'POST'])