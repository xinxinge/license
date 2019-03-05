#!/usr/bin/env python3
'''
功能：公共函数
'''

from flask_restful import fields
from flask import request, g
from flask_restful import marshal
from functools import wraps
import sys, copy, json
import traceback
from app import app, db
from model.baseconfig import Error
from common.const import ReturnCode, LoginSourceType, Action

# 返回数据格式定义
ret_field = {
    'code':    fields.Integer,
    'strcode': fields.String,
    # message: 消息 或 data: 数据
}

def response_marshal(func):
    def inner(*args, **kwargs):
        return marshal(func(*args, **kwargs), g.ret_field)

    return inner

def getlog(msgstr):
    '''输出日志'''
    tbinfo = sys.exc_info()[2]
    if tbinfo == None:
        return ''
    tup = traceback.extract_tb(tbinfo)[-1]
    fname = tup[0].split('/')[-1]
    funcname = tup[2].split('.')[-1]
    if msgstr:
        return '[%s:%d][%s] %s' % (fname, tup[1], funcname, msgstr)
    else:
        return '[%s:%d][%s] no message' % (fname, tup[1], funcname)

def geterr_bystrcode(scode):
    err = Error.query.filter(Error.strcode == scode).first()
    if err == None:
        err = Error(strcode=scode, message=scode)
        db.session.add(err)
        db_write()

    return err

def db_write():
    '''数据提交'''
    try:
        db.session.commit()
        return 0, None
    except Exception as ex:
        db.session.rollback()
        logmsg = getlog(str(ex))
        app.logger.warning(logmsg)
        return -1, str(ex)

def send_msg(scode='succ', msg=''):
    ret = RetMsg()
    ret.setmsg(scode=scode, msg=msg)
    g.ret_field['message'] = fields.String(attribute='msg')

    return ret

def send_dictmsg(data):
    '''根据字典参数设置返回消息
       部分调用的结果已经是格式化的数据
    '''
    ret = RetMsg()
    ret.code = data['code']
    ret.setmsg(data['strcode'], data['message'])
    g.ret_field['message'] = fields.String(attribute='msg')

    return ret

def send_data(data, datafmt=None):
    '''设置返回数据结构'''
    ret = RetMsg()
    ret.data = data
    if datafmt:
        if data:
            g.ret_field['data'] = fields.Nested(datafmt)
        else:
            g.ret_field['data'] = fields.Nested(dict())
    else:
        g.ret_field['data'] = fields.String
    return ret

class RetMsg():
    def __init__(self, scode='succ'):
        err = geterr_bystrcode(scode)
        if scode == 'succ':
            self.code = ReturnCode.succ
        else:
            self.code = ReturnCode.fail
        self.strcode = err.strcode
        self.msg = err.message

    def setmsg(self, scode='succ', msg=''):
        '''设置返回消息'''
        try:
            err = geterr_bystrcode(scode)
            if scode == 'succ':
                self.code = 0
            else:
                self.code = -1
            self.strcode = err.strcode
            if len(msg):
                self.msg = msg
            else:
                self.msg = err.message
        except Exception as ex:
            self.code = 999
            self.strcode = 'unknown'
            self.msg = str(ex)
            logmsg = getlog(str(ex))
            app.logger.info(logmsg)

class JsonData(dict):
    '''POST/PUT参数结构'''

    def __init__(self, jsondata=None):
        if jsondata == None:
            return
        for (k, v) in jsondata.items():
            setattr(self, k, v)

    def check_list(self, keylist):
        '''验证属性列表'''
        for key in keylist:
            if getattr(self, key) == None:
                return key
        return None

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            # logmsg = getlog('NO json key: %s' % name)
            # app.logger.info(logmsg)
            return None

    def __setattr__(self, name, val):
        if hasattr(self, name):
            self[name] = val
        else:
            setattr(self, name, val)

def convert_json(argdict):
    if isinstance(argdict, dict):
        return JsonData(argdict)
    if isinstance(argdict, list):
        data = list()
        for arg in argdict:
            if isinstance(arg, dict):
                data.append(JsonData(arg))
        return data
    return None

def search_json(argdict):
    '''用于从json中解析出搜索使用的参数'''
    if isinstance(argdict, dict):
        redata = dict()
        for k, v in redata.items():
            if len(k.split('__')) == 2:
                redata[k] = v
        return redata
    return dict()

class GetArgs(dict):
    '''GET参数结构'''

    def __init__(self, getargs):
        for k in getargs.keys():
            for v in getargs.getlist(k):
                setattr(self, k, v)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            # logmsg = getlog('NO GET args: %s' % name)
            # app.logger.info(logmsg)
            return None

def getsearchargs(args):
    '''用于从url参数中解析出搜索使用的参数'''
    redata = dict()
    for k, v in args.items():
        if len(k.split('__')) == 2:
            redata[k] = v
    return redata

def update_obj(args, obj, lists):
    ''' 从request中取出参数用于更新实例对象的属性值
        lists表示可以修改的字段的列表
    '''
    for fd in lists:
        value = args.get(fd)
        if value != None and hasattr(obj, fd):
            setattr(obj, fd, value)
        else:
            continue

def set_g_user_login(user, login):
    g.user = {
        'id':   user.id,
        'name': user.name,
        }
    g.login = {
        'id':         login.id,
        'sourcetype': login.sourcetype,
        'token':      login.token
    }

def verify_token(decorated_=None, loginflag=1):
    def _verify_token(func):
        '''登录检查装饰器'''

        @wraps(func)
        def decorated_function(*args, **kwargs):
            if loginflag:
                # 验证,是否有token
                auth_token = request.headers.get('iAuthToken')
                #token是否有效
                from resource.login import isAuthValid
                user, login = isAuthValid(auth_token)
                if user == None:
                    return send_msg('autherror', '未登录')
                set_g_user_login(user, login)

            if request.method in ['POST', 'PUT', 'DELETE']:
                try:
                    if hasattr(request, 'json') and request.json:
                        args[0].jsondata = convert_json(request.json)
                        args[0].searchdata = search_json(request.json)
                    else:
                        args[0].jsondata = JsonData()
                        args[0].searchdata = dict()
                except Exception as ex:
                    logmsg = getlog('argfmt: %s' % str(ex))
                    app.logger.info(logmsg)
                    return send_msg('argfmt', str(ex))
            elif request.method == 'GET':
                args[0].jsondata = GetArgs(request.args)
                args[0].searchdata = getsearchargs(request.args)
            try:
                resp = func(*args, **kwargs)
                return resp
            except Exception as ex:
                logmsg = getlog(str(ex))
                app.logger.info(logmsg)
                return send_msg('syserror', '服务端错误')
        return decorated_function

    if decorated_:
        return _verify_token(decorated_)
    else:
        return _verify_token

# 搜索操作(因该字典与函数关系过于密切，且大概率不会修改，故不在将其放入const文件内)
operators = {
    'eq':       '__eq__',  # 等于
    'gt':       '__gt__',  # 大于
    'ge':       '__ge__',  # 大于或等于
    'lt':       '__lt__',  # 小于
    'le':       '__le__',  # 小于或等于
    'like':     'like',  # like
    'in':       'in_',  # in 例：[1,2,3]
    'contains': 'contains',  # 包含
    'is':       'is_',        # is 与 isnot 只进行测试值是否为空
    'isnot':    'isnot',     #
}

def search_query(entitymodel, searchdict, query=None):
    '''搜索
    利用orm进行搜索
    参数：
    entitymodel： 模型类，例：FloorModel
    searchdict：  字典：例： {‘name__like’: '%北京%'} (name中有北京的元素)
    query:        query 例：Flask.query, 默认为空，为空时会自动生成一个query
    注意：对于searchdict不存在的字段与操作，会自动忽略掉！！！需谨慎操作
    '''
    # 获得query
    if not query:
        query = getattr(entitymodel, 'query')

    for k, v in searchdict.items():
        # 获取filter函数(query.fileter)
        query_filter = getattr(query, 'filter')

        # 获取键值（例：k: id__eq, key=id, op=eq）
        key = k.split('__')[0]
        op = k.split('__')[1]

        # 获取模型属性（表中的列例：FloorModel.id），没有跳过
        if not hasattr(entitymodel, key):
            continue
        column = getattr(entitymodel, key)

        # 查看是否有该操作
        if not operators.get(op, None):
            continue

        # 屏蔽掉前端参数为空的情况
        if v == '' or v == None:
            continue

        # 执行语句 （例：query.filter(FloorModel.id.__eq__(1))）
        if op in ['is', 'isnot']:
            if v == 'None':
                query = query_filter(getattr(column, operators[op])(None))
        elif op in ['in']:
            # 使用in方法，参数必须为list
            if isinstance(v, str):
                v = json.loads(v)
            query = query_filter(getattr(column, operators[op])(v))
        else:
            query = query_filter(getattr(column, operators[op])(v))
    return query


def userlog(resourcename, content, result):
    g.userloglist.append({
        'resourcename':resourcename,
        'content': content,
        'result': result,
    })

@app.before_request
def before_request():
    g.ret_field = copy.deepcopy(ret_field)
    g.userloglist = list()

    # web访问日志
    try:
        raise Exception
    except:
        if len(request.query_string):
            url = '%s %s?%s' % (request.method, request.path,
                    str(request.query_string, encoding='utf8'))
        else:
            url = '%s %s' % (request.method, request.path)
        logmsg = getlog(url)
        app.logger.debug(logmsg)

@app.after_request
def after_request(response):
    from model.baseconfig import UserLogModel
    from common.const import LoginSourceType, Action
    for userlog in g.userloglist:
        ul = UserLogModel(g.user['name'], request.remote_addr, g.login['sourcetype'],
                          None, userlog['resourcename'], getattr(Action, request.method),
                          userlog['content'], userlog['result'])
        db.session.add(ul)
    db.session.commit()
    return response

@app.teardown_request
def teardown_request(response):
    db.session.remove()
    return response


