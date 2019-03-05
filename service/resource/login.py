#!/usr/bin/env python3
'''
功能: 用户登录
'''

from flask_restful import Resource, marshal_with

from common.common import *
from common.const import *
from common.route import *
from common.utils import *
from common.exception import RemoveException
from model.user import UserModel, LoginModel
from flask import g
from resource.user import user_fields
from app import db
from datetime import datetime, timedelta
from model.baseconfig import Parameter

# 返回字段
login_fields = {
    'user':     fields.Nested(user_fields),
    'iAuthToken':  fields.String,
}

class Login(Resource):
    ''' 登录 '''
    resourcename = 'Login'

    @response_marshal
    @verify_token(loginflag=0)
    def post(self):
        ''' 登录认证 '''
        args = self.jsondata
        if not args.username:
            return send_msg('fail', '无用户名')
        if not args.password:
            return send_msg('fail', '无用户密码')
        if args.sourcetype == None:
            return send_msg('fail', '无来源（PC端或者移动端）')
        if int(args.sourcetype) not in [LoginSourceType.pc, LoginSourceType.mobile]:
            args.sourcetype = LoginSourceType.pc

        delete_invalidtoken()

        user = UserModel.query.filter(UserModel.name == args.username).first()
        if not user:
            return send_msg('fail', '用户不存在')

        if user.status == UserStatus.LOCKED:
            return send_msg('fail', '用户已被锁定')

        # 登录错误次数限制
        if not user.verify_password(args.password):
            user.retry_login_count += 1
            if user.retry_login_count >= Parameter.getval('security', 'retry_login_count'):
                user.status = UserStatus.LOCKED
                user.retry_login_count = 0
            db.session.add(user)
            db_write()
            return send_msg('fail', '密码错误')
        user.retry_login_count = 0

        # 登录ip限制
        if not verify_ip(user, request.remote_addr):
            return send_msg('fail', 'ip登录限制')

        # 登录方式限制
        retry_login_type = Parameter.getval('security', 'retry_login_type')
        login = LoginModel.query.filter(LoginModel.userid == user.id,
                                        LoginModel.sourcetype == args.sourcetype).first()
        if retry_login_type == RetryLoginType.allow_retry:
            login = LoginModel()
        elif retry_login_type == RetryLoginType.no_pre_login:
            login = login or LoginModel()
        else:
            if login:
                return send_msg('fail', '不允许重复登录')
            else:
                login = LoginModel()


        login.userid = user.id
        login.ip = request.remote_addr
        login.sourcetype = args.sourcetype
        login.token = generate_token()
        login.createtime = datetime.now()
        login.lasttime = datetime.now()

        data = dict()
        data['iAuthToken'] = login.token
        db.session.add(login)
        db.session.add(user)
        db_write()
        user = UserModel.query.filter(UserModel.name == args.username).first()
        data['user'] = user
        set_g_user_login(user, login)
        userlog(self.resourcename, '用户登录:' + user.name, 'succ')
        return send_data(data, login_fields)

    @response_marshal
    @verify_token
    def delete(self):
        login = LoginModel.query.filter(LoginModel.token == g.login['token']).first()
        user_id = login.userid
        if login:
            login.remove()
            dbflag, dbmsg = db_write()
            if dbflag:
                return send_msg('dberror', dbmsg)
        user = UserModel.query.filter(UserModel.id == user_id).first()
        userlog(self.resourcename, '用户登出:' + user.name, 'succ')
        return send_msg('succ', '成功')

ROUTES.add('login', Login, DEFURL + 'login', ['POST', 'DELETE'])

def random_str(randomlength):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    from random import Random
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def generate_token():
    randstr = random_str(STRING_MEDIUM)
    return randstr

def delete_invalidtoken():
    '''删除失效的token'''
    logins = LoginModel.query.all()
    for login in logins:
        if not isValidLogin(login):
            db.session.delete(login)

def isAuthValid(token):
    login = LoginModel.query.filter(LoginModel.token == token).first()
    curenttime = datetime.now()
    if login and login.ip == request.remote_addr and isValidLogin(login):
        login.lasttime = curenttime
        db.session.add(login)
        db_write()
        return UserModel.query.get(login.userid), login
    return None, None

def isValidLogin(login):
    curenttime = datetime.now()
    free_time = Parameter.getval('security', 'login_free_time')
    valid_time = Parameter.getval('security', 'login_valid_time')
    if curenttime - login.lasttime < timedelta(seconds=free_time) and \
            curenttime - login.createtime < timedelta(seconds=valid_time):
        return True
    return False

def verify_ip(user, ip):
    if user.ip_set['status'] == IpSetStatus.off:
        return True
    it = IP_TEST(ip, user.ip_set['rules'])
    return it.computed()

class IP_TEST:
    def __init__(self, ip, rules):
        self.ip = ip
        self.rules = rules

    def computed(self):
        for rule in self.rules:
            start_ip, end_ip = self.generate_range(rule)
            if self.test(start_ip, end_ip):
                return True
        return False

    def generate_range(self, rule):
        if rule.find('/') != -1:
            t1, t2 = rule.split('/')
            start_ip = t1.split('.')
            end_ip = t1.split('.')
            end_ip[-1] = t2
        elif rule.find('-') != -1:
            s_ip, e_ip = rule.split('-')
            start_ip = s_ip.split('.')
            end_ip = e_ip.split('.')
        else:
            start_ip = rule.split('.')
            end_ip = rule.split('.')
        return start_ip, end_ip

    def test(self, start_ip, end_ip):
        test_ip = self.ip.split('.')
        for start, end, mid in zip(start_ip, end_ip, test_ip):
            if int(mid) < int(start) or int(mid) > int(end):
                return False
        return True
