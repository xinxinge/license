#!/usr/bin/env python3
'''
功能：常量定义
'''

# 版本号
VERSION_NUM = 2.0

# 字符串长度
STRING_SMALL = 16
STRING_MEDIUM = 64
STRING_LARGE = 128
STRING_MAX = 255

# 默认URL地址
DEFURL = '/v1/'


######################################

# 分页时默认每页的数量
PERPAGENUM = 20

class ReturnCode(object):
    '''返回码
    目前只有两种：成功，失败
    '''
    succ = 0
    fail = -1

# 配置管理员
CONFIFURATION_MANAGER_RESOURCES = [
    'Role',
    'RoleList',
    'User',
    'UserList'
]

# 日志管理员
LOG_MANAGER_RESOURCES = [
    'UserLogList'
]

# 默认资源（所有用户均可使用的资源）
DEFAULT_RESOURCES = [
    'MyUser', 'Login'
]

DEFAULT_ROLES = [
    '超级管理员',
    '日志管理员',
    '配置管理员'
]

# 超级管理员的page_set
PAGE_SET = [{"children": [{"title": "userLog"}, {"title": "systemLog"}, {"title": "warnList"}],
                          "title":    "日志管理"}, {"children": [{"title": "warnSetting"}], "title": "系统设置"},
                         {"children": [{"title": "role"}, {"title": "user"}, {"title": "safeSetting"}],
                          "title":    "用户管理"}, {"children": [{"title": "cabmodel"}, {"title": "equipment_model"},
                                                             {"title": "equipment_category"}, {"title": "swCtg"}],
                                                "title":    "基础设置"}]


class LoginSourceType(object):
    '''来源'''
    pc = 0
    mobile = 1

class Action(object):
    '''用户动作'''
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

class Role(object):
    '''用户类型'''
    admin = 1
    peizhi = 2
    rizhi = 3
    richang = 4

class Permission(object):
    read = 1
    write = 2

class ConfirmStatus(object):
    '''确认状态'''
    confirmed = 1
    unconfirmed = 0

class HandleStatus(object):
    '''确认状态'''
    handled = 1
    unhandled = 0

class UserStatus(object):
    ''' 用户状态 '''
    NORMAL = 1
    LOCKED = 2
    INACTIVE = 3

class IpSetStatus(object):
    '''登录ip状态设置'''
    off = 0
    on  = 1

class LoginStatus(object):
    '''登录ip状态设置'''
    off = 0
    on  = 1

class RetryLoginType(object):
    '''重复登录限制'''
    allow_retry = 1  # 允许重复登录
    no_retry = 2     # 禁止重复登录
    no_pre_login = 3 # 自动踢出前一次登录
