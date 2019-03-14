#!/usr/bin/env python3
from app import app, db

# 所有model模块均需添加到列表中，如floor（添加后才可使用flask migrate进行管理）
__all__ = ['baseconfig','user','register']
