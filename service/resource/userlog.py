#!/usr/bin/env python3
'''
功能: 用户日志
'''

from flask import abort, make_response
from flask_restful import Resource, marshal_with

from common.common import *
from common.const import *
from common.route import ROUTES
from common.utils import paging
from model.baseconfig import UserLogModel

from app import db

floor_fields = {
    'id':           fields.Integer(attribute='id'),
    'username':     fields.String(attribute='username'),
    'ip':           fields.String(attribute='ip'),
    'source':       fields.String(attribute='source'),
    'createtime':   fields.String(attribute='createtime'),
    'resourcename': fields.String(attribute='resourcename'),
    'action':       fields.Integer(attribute='action'),
    'content':      fields.String(attribute='content'),
    'result':       fields.String(attribute='result')
}

page_fields = {
    'totalpage': fields.Integer,
    'curpage':   fields.Integer,
    'count':     fields.Integer,
    'items':     fields.List(fields.Nested(floor_fields)),
}

class UserLogList(Resource):
    '''用户日志列表'''
    resourcename = 'UserLogList'

    @response_marshal
    @verify_token
    def get(self):
        '''获取用户日志列表
        '''
        args = self.jsondata

        searchdata = self.searchdata
        query = search_query(UserLogModel, searchdata)
        query = query.order_by(UserLogModel.id.desc())
        cur_page, total_page, count, items = paging(query, args.limit, args.page)
        data = dict()
        data['curpage'] = cur_page
        data['totalpage'] = total_page
        data['count'] = count
        data['items'] = items

        return send_data(data, page_fields)

ROUTES.add('userloglist', UserLogList, DEFURL + 'userlogs', ['GET'])
