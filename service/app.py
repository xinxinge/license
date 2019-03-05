#!/usr/bin/env python3
'''
功能: APP，db初始化
'''
import sys
import os
import logging
import logging.handlers
import yaml
from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

sys.path.extend(('.', 'common', 'model', 'resource', 'api'))

CFGPATH = [sys.path[0], '/etc/ims3d']
CFGFILE = 'config.yaml'
LOGFILE = 'ims3d.log'
# LOG文件大小: 默认16MB
LOGSIZE = 1 << 24
# LOG文件个数
LOGCOUNT = 10


# 设置logging
def _set_logger(flaskapp):
    '''
    设置 Flask app 的logger
    '''
    # 删除 Flask 的默认 Handler
    del flaskapp.logger.handlers[:]

    #print(logging.getLogger('root').__dict__)
    if flaskapp.debug:
        # DEBUG模式
        flaskapp.logger.setLevel(logging.DEBUG)
    else:
        flaskapp.logger.setLevel(logging.INFO)
    # log格式
    logformat = '[%(asctime)s][%(levelname)s]%(message)s'
    timeformat = '%Y/%m/%d %H:%M:%S'
    logfmt = logging.Formatter(fmt=logformat, datefmt=timeformat)

    # uwsgi关闭日志, 全部输出到stream中
    syshdl = logging.StreamHandler()
    syshdl.setFormatter(logfmt)
    # 创建本地循环日志文件
    logname = os.path.join(sys.path[0], LOGFILE)
    filehdl = logging.handlers.RotatingFileHandler(logname,
            maxBytes=LOGSIZE, backupCount=LOGCOUNT, encoding='utf8')
    filehdl.setFormatter(logfmt)

    # SQL LOG:
    # [sqlalchemy, sqlalchemy.engine sqlalchemy.dialects,
    #  sqlalchemy.pool, sqlalchemy.orm]
    sqllogger = logging.getLogger('sqlalchemy')
    if sqllogger:
        sqllogger.setLevel(logging.WARNING)
    # 设置logger
    for log in (flaskapp.logger, sqllogger):
        for hdl in (syshdl, filehdl):
            if log and hdl:
                log.addHandler(hdl)

def get_sysconfig(app):
    '''获取系统配置'''
    flag_cfgfile = 0
    for pth in CFGPATH:
        filename = os.path.join(pth, CFGFILE)
        if os.path.isfile(filename):
            with open(filename, 'r') as fp:
                dbcfg = yaml.load(fp.read())
                flag_cfgfile = 1
            break
    if flag_cfgfile == 0:
        print('Can\'t find config file!')
        sys.exit()

    try:
        if dbcfg['dbtype'] == 'mysql':
            if dbcfg['dbpass']:
                connstr = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8'\
                        % (dbcfg['dbuser'], dbcfg['dbpass'],\
                           dbcfg['dbhost'], dbcfg['dbname'])
            else:
                connstr = 'mysql+pymysql://%s@%s/%s?charset=utf8'\
                        % (dbcfg['dbuser'], dbcfg['dbhost'], dbcfg['dbname'])
            app.config['SQLALCHEMY_POOL_SIZE'] = 10
            app.config['SQLALCHEMY_POOL_TIMEOUT'] = 180
            # for mysql: 默认300秒回收空闲连接
            app.config['SQLALCHEMY_POOL_RECYCLE'] = 300
            app.config['SQLALCHEMY_POOL_PRE_PING'] = True
        elif dbcfg['dbtype'] == 'sqlite':
            connstr = 'sqlite:///' + os.path.join(pth, 'data.sqlite')
        else:
            print('Unsupported dbtype')
            sys.exit()

        app.config['SQLALCHEMY_DATABASE_URI'] = connstr
        app.config['SQLALCHEMY_MIGRATE_REPO'] = 'db_resository'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['dbtype'] = dbcfg['dbtype']
        if 'debug' in dbcfg and dbcfg['debug'] == 1:
            app.debug = True
    except KeyError as ke:
        print('-- %s --' % filename)
        print('Need configuration: %s' % ke)
        sys.exit()

#app = MyFlask(__name__)
app = Flask(__name__)
app.debug = False

# 获取系统配置
get_sysconfig(app)

_set_logger(app)

# 数据库接口
class MyAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        if app.config['dbtype'] == 'mysql':
            options.update({
                'isolation_level': 'READ COMMITTED',
                })
        super(MyAlchemy, self).apply_driver_hacks(app, info, options)
# flask-sqlalchemy错误: Query-invoked autoflush
options = {'autoflush': False}
db = MyAlchemy(app, session_options=options)

api = Api(app)