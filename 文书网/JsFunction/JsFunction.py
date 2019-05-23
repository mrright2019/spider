#coding:utf-8
import execjs
import requests
import PyV8 
import js2py
import sys
sys.path.append("..")
from Config import *
#初始化js函数体
ctxt = PyV8.JSContext() #JSV8  unzip
ctxt.enter() 

mode_path = ""

a = open(App_Path+"JsFunction/pako.js","r").read()
b = open(App_Path+"JsFunction/aes.js","r").read()
c = open(App_Path+"JsFunction/com.js","r").read()

ctxt.eval(a)

context = js2py.EvalJs() #js2py Navi
context.execute(b+c)


def CreateGuid():
	with open(App_Path+'JsFunction/createguid.js') as fp:
		js = fp.read()
		ect = execjs.compile(js)
		# guid = ect.call('createGuid')
		guid = ect.call('createGuid') + ect.call('createGuid') + "-" + ect.call('createGuid') + "-" + ect.call('createGuid') + ect.call('createGuid') + "-" + ect.call('createGuid') + ect.call('createGuid') + ect.call('createGuid')
		return guid

def unzip(_id):
	return ctxt.locals.unzip(_id) 


# def get_vl5x(vjkl5):
# 	with open(App_Path+'JsFunction\\vl5x.js') as fp:
# 		js = fp.read()
# 		ctx = execjs.compile(js)
# 	vl5x = (ctx.call('GetVl5x',vjkl5))
# 	return vl5x


def Decry(runal,_id):
	unzipid = unzip(_id)
	context.setkey(runal)
	return context.Navi(unzipid)
import re

def get_ase_key(reval):
	unziprev = unzip(reval)
	# print unziprev
	str1, str2 = re.findall('\$hidescript=(.*?);.*?\((.*?)\)\(\)', unziprev)[0]
	# print str1
	# print "--------------------------------"
	# print str2
	js_func = str2.replace('$hidescript', str1)
	aes_key = execjs.eval(js_func)
	if not aes_key:
	    import js2py
	    aes_key = js2py.eval_js(js_func)
	aes_key = re.findall('com.str._KEY=\"(.*?)\";', aes_key)[0]
	return aes_key



def get_vl5x(key):
	with open(App_Path+'JsFunction/getkey.js') as fp:
	    js = fp.read()
	    ctx = execjs.compile(js)
	    vl5x = ctx.call("getKey", key)
	    return vl5x



# key = "580c99ff42bf1101ed18151601539b9d399fa94a"
# print get_vl5x(key)
# print getKey(key)
# exit()
if __name__ == "__main__":
	# print CreateGuid()
	_id = "DcOPw4cNw4BADAPDgcKWwpTDg1PDqcO6L8OJw74TGMOuSsKLOcKrwrdnwpPDi8K0wojCmTnCqGUSLsKZeyLDpizDukVPLR7DhsKbY8OFwrLDqiTDpxpgworDkgI2e8KRN3XChcOZwqJow6DCscOxw4pow6DDtDTDjjPDslXCncOTPQRRwofCgsOKMsOVw53Cq0HDn19JWMKqLsKOBMOew73DoRrClsOgf8Oqw6BtDTnCvgvCtMOCw7/Dnx/DviN6V1DDuirCh8OowoXCm8KGH3w="
	# print Decry("f056cdc1f00c4bf98a46f37db26d4b51",_id)
	runeval = "w61aQW7CgzAQfAtRDsK2wqjDugHClFPCnsOQw6MKwqHCiiQNwofChsOKwqHCpyh/L8OQwoQaMMOBwqnDgThhJMK0CHvCvTszXsObIMKxw5wnwpvDrTEWw4lXwrZ6w4tEcsO4eMOdwonDtHPCvX8Xw6t0wrNlwr7Dp1MIw6PCtHnCgQgww7PCqMKQZyAywpPDpcKKXQlzCwPDncKhLAxmD8KKYXJBHcKsQRgiQB3DiAHDvlACwppAGMOoBHLCoMKEGcKAQSE4aHgQRMKrRcKcHsKOwpnDuMKOwrNULMKCwojCojDCvxjDs0/Dp8OCwq3Cuk5nTsK/Iyk3YcOoM8Kvw6zDoFTCj1l0w7TDt8KUwo/Di8K/wr8TwogVw43CuQd5RQ/ChcKUw58aCcOrw67DnmVAd8KyBm7CpcOvTUxyNHV7wpXCqkTDncKWwqgFQcOJw6FGw6wKwqTCnsKiw5JjL2xNwo97w5zDrsO2w73DnwDCg1HCpkPDq8K1dS1Twq3DojfDizlcwpDCgSMNw4nCjmksRcKHWMOrVcOESCktRB8twoUFw5jDo1TCucK0wqErw4vDlibCuSp5w48BaMK5JMKrw6QdR2JDwqtRw7fDiynDpsOjw5HClsK7wr3CtTjDoTLCscOMw5TDtMO1w4LCtjLDvWknw4LDtBzClTLCq3APCMOgwoLCosO7aHIGwqTCpl7Cig/DgRY5wqrCvRzCqFvDpcKAZMOwKcOrwpB4w4AjwqXDpcKMBz8="
	print(unzip(runeval))
	# print(Decry(asekey,_id))
	# print(asekey)