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
Register_fields = {
    'name':              fields.String,
    'code':              fields.String,
    'Serial_id':         fields.String,
    'day':               fields.Integer,
    'date':              fields.DateTime,

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
        if args.code in 'TEST':
            lic.setLicType(0)#状态
        else:
            lic.setLicType(1)  # 状态
        lic.setCustomer(args.name)#客户名称
        lic.setMaxCabinet(args.count)#独有属性如有机柜数
        lic.setProductid(args.code)#序列号
        if not args.date:
            time=datetime.date.today().isoformat()
        else:
            time=args.date
        lic.setValidation(time,args.day)#有效期
        lic.encrypt_keystr()
        msg=lic.getkey()
        # msg= uuid.uuid3(uuid.NAMESPACE_DNS,args.name)#根据序列号生成注册码 v
        if not msg:
            return send_msg('fail', '注册码获取失败')
        # create_time=datetime.datetime.now()#获取系统当前时间
        # delta=datetime.timedelta(days=args.day)
        # last_access_time = (create_time + delta).strftime("%Y--%m--%d %H:%M:%S")
        #计算有效时间
        newuser = RegisterModel(args.name,args.date,args.day,str(msg),args.code,args.abbreviation)
        db.session.add(newuser)
        dbflag, dbmsg = db_write()
        if dbflag:
            return send_msg('dberror', dbmsg)
        return send_msg('succ', str(msg))

    @response_marshal
    @verify_token(loginflag=0)
    def get(self):
        # args = self.jsondata
        # query = RegisterModel.getlist()
        # cur_page, total_page, count, items = paging(query, args.limit, args.page)
        # data = dict()
        # data['curpage'] = cur_page
        # data['totalpage'] = total_page
        # data['count'] = count
        # data['items'] = items
        data = RegisterModel.getlist()
        # RegisterModelgetlist
        return send_data(data, Register_fields)

    @response_marshal
    @verify_token(loginflag=0)
    def delete(self):
        '''删除'''
        args = self.jsondata
        RegisterModel.deletecode(args.code)





class Serial_number(Resource):
    resourcename = 'Serial_number'
    @response_marshal
    @verify_token(loginflag=0)
    def post(self):
        ars=self.jsondata

        num= RegisterModel.query.filter(RegisterModel.abbreviation==ars.abbreviation).all()
        if not num:
            index = 1
        else:
            index = len(num)
        zf=ars.abbreviation+ars.test+str(index)
        nums = 10 - len(zf)
        msg=ars.abbreviation + ars.test + '0'*nums+ str(index)
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

ROUTES.add('Register_code', Register_code, DEFURL + 'Register_code', [ 'GET','POST','DELETE'])
ROUTES.add('Product_list', Product_list, DEFURL + 'Product_list', ['GET','POST'])
ROUTES.add('Serial_number', Serial_number, DEFURL + 'Serial_number', [ 'POST'])