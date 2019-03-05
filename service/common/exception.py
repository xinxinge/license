# !/usr/bin/env python3
'''
功能: 异常
'''

class RemoveException(BaseException):
    ''' 删除异常 '''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class EquipmentStateException(BaseException):
    ''' 设备状态异常 '''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class CreateException(BaseException):
    ''' 设备状态异常 '''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg