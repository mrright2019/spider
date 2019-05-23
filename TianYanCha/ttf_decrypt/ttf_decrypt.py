#coding:utf-8
import __init__
from ocr import *
import freetype
import numpy as np
import json
from PIL import Image
import copy
import os
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

class ttf(object):

	def __init__(self,filename,corn = "baidu"):
		self.filename = filename
		self.face = freetype.Face(filename)
		self.face.set_char_size(48*64)
		self.json_file = filename+".json"
		try:
			with open(self.json_file,'r') as jf:
				self.ttf_json = json.load(jf)
		except:
			self.ttf_json = {}
		# self.ttf_json = {}
		# print self.ttf_json
		self.ocr = ocr_creator(corn)

	def decrypt(self,key):
		# print key
		if self.ttf_json.has_key(key):
			return self.ttf_json[key]
		self.face.load_char(key)
		bitmap = self.face.glyph.bitmap
		buf = copy.deepcopy(bitmap.buffer)
		if len(buf) == 0:
			return key
		img = np.array(buf)
		# print bitmap.rows,bitmap.width
		img.resize((bitmap.rows,bitmap.width))
		im = Image.fromarray(np.uint8(img))
		im = im.convert('RGB')
		bg = Image.new("RGB",(60+bitmap.width,60+bitmap.rows))
		box = (30,30)
		bg = bg.convert("RGB")
		bg.paste(im,box)
		bg.save("key.jpg")
		# im.save("key.jpg")
		res = self.ocr.ocr("key.jpg")
		self.ttf_json[key] = res
		self._save()
		return res

	def _save(self):
		with open(self.json_file,'w') as f:
			json.dump(self.ttf_json,f)



if __name__ == "__main__":
	t = ttf("../TTF/3374746763d33cf2781e18814b935876.ttf")
	# for i in range(0,10):
	a = t.decrypt(u"别")
	print(a.encode("utf-8"))
	# for i in range(10):
	# 	print t.decrypt(str(i))
