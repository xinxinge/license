#!/usr/bin/env python3
from app import app, db

# 所有resource模块均需添加到列表中，如floor（添加后才会加入路由进行）
__all__ = ['param', 'userlog', 'user', 'login','register']
