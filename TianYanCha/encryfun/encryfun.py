#coding:utf-8

import hashlib

def md5(s):
	md5 = hashlib.md5(s.encode('utf-8')).hexdigest()
	return md5


# print md5("a")