#coding:utf-8
from aip import AipOcr
from pyocr import pyocr
from PIL import Image

import httplib
import md5
import urllib
import urllib2
import random
import json
import base64
def ocr_creator(classname="sougou"):
	if classname == "sougou":
		return sougou_ocr()
	if classname == "baidu":
		return baidu_ocr()
	if classname == "tess":
		return tess_ocr()

class baidu_ocr(object):

	def __init__(self):
		self._app_id = "14844924"
		self._app_secret_key = "ofSTq2CDz0syaQkbDBdeqauqRbVH4DKV"
		self._app_key = "dsAEpphD07XdDYwktjfxAYIZ"
		self.client = AipOcr(self._app_id ,self._app_key ,self._app_secret_key )
		# print help(self.client)

	def ocr(self,filename):
		fdata = open(filename,"rb").read()
		options={
			'detect_direction':'true',
			'language_type':'CHN_ENG',
			'detect_direction':'false',
		}
		result = self.client.basicGeneral(fdata,options)
		# print(result)
		return result['words_result'][0]['words']


class sougou_ocr(object):
	def __init__(self):
		self.appKey = '730d71c021593e28'
		self.secretKey = 'BwvvWpNasjldDW5bumxqDc5fyshxQ68E'
		self.httpClient = None


	def ocr(self,filename):
		try:
		    f=open(filename,'rb') #二进制方式打开图文件
		    img=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
		    f.close()
		    detectType = '10012'
		    imageType = '1'
		    langType = 'zh-en'
		    salt = random.randint(1, 65536)
		    sign = self.appKey+img+str(salt)+self.secretKey
		    m1 = md5.new()
		    m1.update(sign)
		    sign = m1.hexdigest()
		    data = {'appKey':self.appKey,'img':img,'detectType':detectType,'imageType':imageType,'langType':langType,'salt':str(salt),'sign':sign}
		    data = urllib.urlencode(data)
		    req = urllib2.Request('http://openapi.youdao.com/ocrapi',data)
		    response = urllib2.urlopen(req)
		    print response.read()
		    result = json.loads(response.read())
		    # print result
		    return result["Result"]["regions"][0]["lines"][0]["text"]
		except Exception, e:
		    pass




class tess_ocr(object):
	def __init__(self):
		pass

	def ocr(self,filename):
		tools = pyocr.get_available_tools()[:]
		if len(tools) == 0:
			print("No Ocr tool")
		return tools[0].image_to_string(Image.open(filename),lang='chi_sim')
		# return


if __name__ == '__main__':
	bo = baidu_ocr()
	response = bo.ocr("../ttf_decrypt/key.jpg")
	print response
	# print response['words_result'][0]['words']