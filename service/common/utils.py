#!/usr/bin/env python3
'''
功能: 工具
'''

import math
import xlrd
from common.const import PERPAGENUM
from flask_sqlalchemy import BaseQuery
from zipfile import ZipFile
from io import BytesIO
from PIL import Image

def paging(query, perpagenum, curpage):
    '''分页函数
    不检查参数
    可为flask_sqlalchemy.BaseQuery类型和list类型提供分页
    参数：
        query： sqlalchemy的query 或 普通的list
        perpagenum： 每页的数量
        cur_page: 页数（默认1）
    返回：
        返回一个元组
        分别是：当前页码 总页码 总数 元素列表
    '''
    # 不分页(只分一页)
    if perpagenum != None and int(perpagenum) == 0:
        if isinstance(query, BaseQuery):
            count = query.count()
        else:
            count = len(query)
        datas = query
        return 1, 1, count, datas

    if perpagenum:
        perpagenum = int(perpagenum)
    else:
        perpagenum = PERPAGENUM

    if curpage:
        curpage = int(curpage)
    else:
        curpage = 1

    if isinstance(query, BaseQuery):
        count = query.count()
        datas = query.limit(perpagenum).offset((curpage - 1) * perpagenum)
    else:
        count = len(query)
        datas = query[(curpage - 1) * perpagenum: \
                      (curpage - 1) * perpagenum + perpagenum]

    totalpage = math.ceil(count / perpagenum)
    return curpage, totalpage, count, datas

class ZipFileReader():
    '''用于读取.3source文件
    获取相应的设备图片等
    '''
    PWD = b'3source.cn'
    IMAGES = 'images'
    PRODUCT = 'product.xls'
    FILES_RSO = 'rso'
    FILES_DB = 'db'

    def __init__(self, file_contents):
        self.zip_file = ZipFile(BytesIO(file_contents), "r")

    def get_image(self, image_name):
        image_file = self.IMAGES + "/" + image_name
        return Image.open(BytesIO(self.get(image_file)))

    def get_xls_wb(self):
        return xlrd.open_workbook(file_contents=self.get(self.PRODUCT))

    def get(self, name):
        try:
            return self.zip_file.read(name, self.PWD)
        except:
            raise ValueError(u"升级模块内容错误，无法获取数据文件: %s" % name)

    def get_3d_files(self):
        results = []
        for n in self.zip_file.filelist:
            if n.filename.endswith(self.FILES_RSO) and n.flag_bits:
                results.append(n.filename)
            elif n.filename.endswith(self.FILES_DB) and n.flag_bits:
                results.append(n.filename)
        return results


if __name__ == '__main__':
    print('分页函数（paging）测试：')
    li = [1, 2, 3, 4, 5, 6, 7, 8]
    print('list：')
    print(li)
    print('第二页（每页两个元素,返回的格式：页数，总数，元素列表）：')
    print(paging(li, 2, 2))
    print('utils.py')
