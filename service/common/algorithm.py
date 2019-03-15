import base64
import datetime
import uuid
from Crypto.Cipher import AES
from flask_restful.representations import json

aes_key = b'3Source3Ddcimsys'
aes_iv = b'3DdcimisveryGood'

LIC_ONTRIAL = 0     # 试用
LIC_OFFICIAL = 1    # 正式
class License:
    def setProductid(self, prd_id):
        self.data['prd_id'] = prd_id

    def setCustomer(self, customer):
        self.data['customer'] = customer

    def setLicType(self, lictype=LIC_ONTRIAL):
        '''设置license类型'''
        self.data['lic_type'] = lictype

    def setMaxCabinet(self, maxnum):
        '''设置机柜数'''
        self.data['max_cab'] = maxnum

    def setValidation(self, regdate=None, days=30):
        '''设置有效期'''
        if regdate:
            self.data['reg_date'] = regdate
        self.data['valid_days'] = days



    def getkey(self):
        newlic = self.data.copy()
        return newlic['lickey']
    def getInfo(self):
        '''输出license信息'''
        newlic = self.data.copy()
        if 'random' in newlic:
            del newlic['random']
        if 'lickey' in newlic:
            del newlic['lickey']
        if newlic['reg_date'] != '0000-00-00':
            regdate = datetime.datetime.strptime(
                    newlic['reg_date'], '%Y-%m-%d')
            enddate = regdate + datetime.timedelta(days=newlic['valid_days'])
            newlic['end_date'] = enddate.date().isoformat()
        else:
            newlic['end_date'] = newlic['reg_date']
        # license状态
        newlic['status'] = self.checkLicense()

        return newlic

    def checkLicense(self):
        '''license状态: 0 - 有效; 1 - 无效'''
        if self.data['lic_type'] == LIC_OFFICIAL:
            return 1
        if self.data['reg_date'] != '0000-00-00':
            regdate = datetime.datetime.strptime(
                    self.data['reg_date'], '%Y-%m-%d')
            tmdiff = datetime.datetime.today() - regdate
            if tmdiff.days <= self.data['valid_days']:
                return 1

        return 0
    def __init__(self, flag=0):
        self.data = dict()
        if flag:
            # 默认测试license
            # 产品ID
            self.setProductid('DCTEST001')
            # 客户名称
            self.setCustomer('测试')
            # 注册类型
            self.setLicType(LIC_ONTRIAL)
            # 最大机柜数
            self.setMaxCabinet(100)
            # 注册日期
            regdate = datetime.date.today().isoformat()
            # 有效天数: 30
            self.setValidation(regdate, 30)
        else:
            # 无效license
            # 产品ID
            self.setProductid(u'未知')
            # 客户名称
            self.setCustomer(u'未知')
            # 注册类型
            self.setLicType(LIC_ONTRIAL)
            # 最大机柜数
            self.setMaxCabinet(0)
            # 注册日期
            regdate = '0000-00-00'
            # 有效天数: 0
            self.setValidation(regdate, 0)

    def encrypt_keystr(self):
        '''加密licdata'''
        global aes_key, aes_iv
        if 'lickey' in self.data:
            return
        # 随机字符串, 防止一样的注册码
        self.data['random'] = str(uuid.uuid4())
        try:
            obj = AES.new(aes_key, AES.MODE_CBC, aes_iv)
            lictxt = json.dumps(self.data, ensure_ascii=False)
            if len(lictxt) % 16:
                padlen = 16 - len(lictxt) % 16
                lictxt = lictxt + ''.zfill(padlen)
            keydata = obj.encrypt(lictxt)
            self.data['lickey'] = base64.b64encode(keydata)

        except Exception as err:
            print (str(err))


    def decrypt_keystr(self, keystr):
        '''解密keystr'''
        global aes_key, aes_iv
        licdata = dict()

        try:
            obj = AES.new(aes_key, AES.MODE_CBC, aes_iv)
            keydata = base64.b64decode(keystr)
            lictxt = obj.decrypt(keydata)
            padpos = lictxt.find('}0') + 1
            if padpos == 0:
                jsdata = json.loads(lictxt)
            else:
                jsdata = json.loads(lictxt[:padpos])
            if jsdata != None:
                for (k, v) in jsdata.items():
                    licdata[k] = v
        except Exception as err:
            print(str(err))

        return licdata

    def __repr__(self):
        return json.dumps(self.data, ensure_ascii=False)
