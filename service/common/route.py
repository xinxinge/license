#!/usr/bin/env python3
'''
功能: 路由表
'''

class Routes():
    '''路由表'''

    def __init__(self):
        '''初始化'''
        self.routedict = dict()

    def add(self, name, classname, url, methods):
        d = dict()
        d['class'] = classname
        d['url'] = url
        d['methods'] = methods
        self.routedict[name] = d

ROUTES = Routes()

if __name__ == '__main__':
    t = Routes()
    print(t.routedict)
    print('template.py')
