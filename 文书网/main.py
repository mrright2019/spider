#coding:utf-8
import sys
from JsFunction import *
from Spider import *
from Config import *
from gevent import monkey; monkey.patch_all()
import gevent
import time
import requests
from Saver import *
requests.adapters.DEFAULT_RETRIES = 10
NextIp = -1
RemindKey = 0
NoNext = 1
HaveNext = 2



def GetVCode( req = requests,proxies = None):
	guid = CreateGuid()
	# print guid
	data = {
		"guid":guid,
	}
	res = req.post("http://wenshu.court.gov.cn/ValiCode/GetCode",data=data,headers=headers, proxies = proxies)#,timeout=10)
	print res.text
	if res.status_code == 200:
		return guid,res.text
	else:
		# time.sleep(60)
		return GetVCode( proxies = proxies)

import datetime

def getday(today,n):
    the_date = datetime.datetime.strptime(today, '%Y-%m-%d')
    result_date = the_date + datetime.timedelta(days=n)
    d = result_date.strftime('%Y-%m-%d')
    return d




def getVl5x(req = requests, proxies = None):
	# print("vl5x")
	guid,vcode = GetVCode( req = req,proxies = proxies)
	# print(guid,vcode)
	res2 = req.get("http://wenshu.court.gov.cn/list/list/?sorttype=1&number="+vcode+"&guid="+guid+"&conditions=searchWord+1+WSLX++%E6%96%87%E4%B9%A6%E7%B1%BB%E5%9E%8B:%E5%88%A4%E5%86%B3%E4%B9%A6&conditions=searchWord+002001+AY++%E6%A1%88%E7%94%B1:%E4%BA%BA%E6%A0%BC%E6%9D%83%E7%BA%A0%E7%BA%B7&conditions=searchWord++CPRQ++%E8%A3%81%E5%88%A4%E6%97%A5%E6%9C%9F:2018-07-01%20TO%202018-10-28",headers=headers, proxies = proxies)#,timeout=8)
	print(res2)
	if res2.status_code == 200:
		# print("cookies url",res2)
		# print(res2.content)
		# print(res2.cookies)
		vjkl5 = res2.cookies["vjkl5"]
		vl5x = get_vl5x(vjkl5)
		return guid,vcode,vl5x,res2.cookies
	else:
		print("vl5x2 staute is not 200")
		print(res2.cookies)
		return getVl5x(req = req, proxies = proxies)


def GetContentByDay(begindate,enddate,page=1,vlen=4, proxies = None,s = requests,saver = None):
	# print proxies
	# guid,vcode,vl5x,cookies = getVl5x(req = s, proxies = proxies)
	# print guid,vcode,vl5x,cookies
	try:
		guid,vcode,vl5x,cookies = getVl5x(req = s, proxies = proxies)
		# print(guid,vcode,vl5x,cookies)
	except Exception as e:
		print(e)
		print("Error Function : getVl5x")
		return NextIp
	data = {
		"guid":guid,
		"number":vcode[:vlen],
		"Page":10,
		"Index":page,
		"Direction":"asc",
		"Order":"裁判日期",
		"Param":"案件类型:民事案件,案由:人格权纠纷,法院层级:基层法院,文书类型:判决书,裁判日期:"+begindate+"   TO   "+enddate,
		"vl5x":vl5x,
	}
	# print data
	try:
		response = s.post("http://wenshu.court.gov.cn/List/ListContent",data=data,headers=headers,cookies=cookies, proxies = proxies,timeout=10)
	except Exception as e:
		print(e)
		return NextIp
	# print(response.content)
	if response.text == "\"remind key\"":
		return RemindKey
	if response.text == "\"remind\"":
		return NextIp
	RunEval = re.findall('\\\\"RunEval\\\\":\\\\"(.*?)\\\\",', response.text)
	if len(RunEval)==0:
		if u"360安域" in response.text:
			# time.sleep(20)
			print(u"360")
			return NextIp
		# print("RunEval")
		return NoNext
	RunEval = RunEval[0]
	IdList = re.findall('\\\\"文书ID\\\\":\\\\"(.*?)\\\\"',response.content)
	asekey = get_ase_key(RunEval)
	# print("ase_key:",asekey)
	for _id in IdList:
		DocID = Decry(asekey,_id)
		try:
			saver = SaverRedis(host="140.143.251.186")
			saver.save(DocID)
			print DocID
		except Exception as e:
			print e
	if len(IdList) <10:
		return NoNext
	return HaveNext

