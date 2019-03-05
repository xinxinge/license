#!/usr/bin/env python3
'''
功能: 数据库管理
根据model创建数据库，更新数据库

1.初始化（如之前已有 migrations文件夹需删除 ，同时需删除数据库中的表alembic_version）
    python manager.py init

2.更新数据库
    python manager.py upgrade
'''
import sys
import os
import shutil

from flask_migrate import Migrate, init, migrate, upgrade

from common.common import db_write
from app import app, db
from model import *

# 激活flask程序上下文
ctx = app.app_context()
ctx.push()

MIGDIR = './migrations'
class Ims3dMigrate():
    '''数据库迁移类'''

    def __init__(self):
        '''初始化'''
        self.migrate = Migrate(app, db)

    def db_init_const(self):
        # 为数据表添加初始化数据

        from model.user import UserModel
        if UserModel.query.count() == 0:
            # 添加管理员
            UserModel.db_init()


        # 系统配置
        from resource.param import Sysconfig

        Sysconfig.set_default()

        dbflag, dbmsg = db_write()

        if dbflag:
            print('Failed to add constant data:', dbmsg)
        else:
            print('Succeeded to add constant data')

    def db_init(self):
        '''数据库初始化'''
        init(directory=MIGDIR)
        migrate(directory=MIGDIR)
        db.create_all()
        self.db_init_const()

    def db_upgrade(self):
        '''数据库升级'''
        migrate(directory=MIGDIR, splice=True)
        upgrade(directory=MIGDIR)

    def db_drop(self):
        db.drop_all()
        if os.path.exists(MIGDIR):
            shutil.rmtree(MIGDIR)
        else:
            print('No such dir: %s' % MIGDIR)

    def run(self, argv):
        if len(argv) > 1:
            if argv[1] in ['init', 'upgrade', 'drop']:
                eval('self.db_{}()'.format(argv[1]))
                return

        print('Usage: python manager.py <init|upgrade>')

if __name__ == '__main__':
    db.create_all()
    im = Ims3dMigrate()
    im.run(sys.argv)

