#!/usr/bin/env python3
'''
功能: 用户
'''

from flask_restful import Resource, marshal_with

from common.common import *
from common.const import *
from common.route import *
from common.utils import *
from common.exception import RemoveException
from model.user import UserModel, LoginModel
from app import db

user_fields = {
    'id':       fields.Integer,
    'name':     fields.String,
    'email': fields.String,
    'create_time': fields.DateTime,
    'ip_set': fields.Raw(),
    'last_access_time': fields.DateTime,
    'status': fields.Integer,
}

# 分页返回字段
page_fields = {
    'totalpage': fields.Integer,
    'count':     fields.Integer,
    'page':      fields.Integer,
    'items':     fields.List(fields.Nested(user_fields)),
}

class User(Resource):
    ''' 用户 '''
    resourcename = 'User'

    @response_marshal
    @verify_token
    def get(self, user_id):
        ''' 获取指定用户信息 '''
        park = UserModel.get_by_id(user_id)

        if not park:
            return send_msg('fail', '不存在的用户')
        return send_data(park, user_fields)

    @response_marshal
    @verify_token
    def put(self, user_id):
        ''' 修改指定用户信息 '''
        user = UserModel.get_by_id(user_id)
        if not user:
            return send_msg('fail', '不存在的用户')

        args = self.jsondata
        fds = ['email', 'ip_set', 'status']  # 可修改的字段
        update_obj(args, user, fds)
        db.session.add(user)
        dbflag, dbmsg = db_write()
        if dbflag:
            return send_msg('dberror', dbmsg)
        userlog(self.resourcename, '修改用户（属性）:' + user.name, 'succ')
        return send_msg('succ')

class UserList(Resource):
    resourcename = 'UserList'

    @response_marshal
    @verify_token
    def get(self):
        ''' 获取用户列表，并进行分页
            可以根据name, address进行查询
         '''
        args = self.jsondata
        searchdata = self.searchdata
        query = search_query(UserModel, searchdata)

        page, page_nums, count, parks = paging(query, args.limit, args.page)
        data = dict()
        data['page'] = page  # 当前页码
        data['totalpage'] = page_nums  # 总页数
        data['count'] = count
        data['items'] = parks

        return send_data(data, page_fields)

    @response_marshal
    @verify_token
    def post(self):
        ''' 创建用户 '''
        args = self.jsondata
        if not args:
            return send_msg('fail', '无json数据')

        if not args.name:
            return send_msg('fail', '无参数name')
        if not args.password:
            return send_msg('fail', '无参数password')
        if not args.email:
            return send_msg('fail', '无参数email')

        user = UserModel.query.filter_by(name=args.name).first()
        if user:
            return send_msg('fail', '用户名已被占用')

        newuser = UserModel(args.name, args.password, args.email)
        db.session.add(newuser)

        dbflag, dbmsg = db_write()
        if dbflag:
            return send_msg('dberror', dbmsg)
        userlog(self.resourcename, '新建用户:' + args.name, 'succ')
        return send_msg('succ')

    @response_marshal
    @verify_token
    def delete(self):
        ''' 根据id列表批量删除用户
            自动忽略不存在的用户
         '''
        args = self.jsondata
        if not args:
            return send_msg('fail', '无json数据')

        ids = args.get('dtlist')
        names = []
        for _id in ids:
            try:
                user = UserModel.get_by_id(_id)
                if user:
                    names.append(user.name)
                    user.remove()
            except RemoveException as ex:
                userlog(self.resourcename, '删除用户:' + user.name, 'fail')
                return send_msg(ex.msg)
        dbflag, dbmsg = db_write()
        if dbflag:
            return send_msg('dberror', dbmsg)
        userlog(self.resourcename, '删除用户:' + ','.join(names), 'succ')
        return send_msg('succ')

class MyUser(Resource):
    ''' 自己的信息 '''
    resourcename = 'MyUser'

    @response_marshal
    @verify_token
    def get(self):
        ''' 获取本人用户信息 '''
        user = UserModel.query.filter(UserModel.id == g.user['id']).first()
        return send_data(user, user_fields)

    @response_marshal
    @verify_token
    def put(self):
        ''' 修改用户自身信息 '''
        user = UserModel.query.filter(UserModel.id == g.user['id']).first()
        args = self.jsondata
        # 修改密码
        if args.newpassword and args.oldpassword:
            if not user.verify_password(args.oldpassword):
                return send_msg('fial', '密码错误')
            user.password = args.newpassword
            login = LoginModel.query.filter(LoginModel.id == g.login['id']).first()
            login.remove()
            db.session.add(user)
            dbflag, dbmsg = db_write()
            if dbflag:
                return send_msg('dberror', dbmsg)
            return send_msg('succ')

        fds = ['email', 'ip_set']  # 可修改的字段
        update_obj(args, user, fds)
        db.session.add(user)
        dbflag, dbmsg = db_write()
        if dbflag:
            return send_msg('dberror', dbmsg)
        userlog(self.resourcename, '修改用户（属性）:' + user.name, 'succ')
        return send_msg('succ')

ROUTES.add('users', UserList, DEFURL + 'users', ['GET', 'POST', 'DELETE'])
ROUTES.add('user', User, DEFURL + 'user/<int:user_id>', ['GET', 'PUT'])
ROUTES.add('myuser', MyUser, DEFURL + 'myuser', ['GET', 'PUT'])
