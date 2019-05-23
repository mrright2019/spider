#coding:utf-8

from Saver import *
import requests
from Config import *
import os
import time
import threading
import MySQLdb

NotId = 1
ExistId = 2
DownError=0

def GetIp():
	getting = True
	url = "http://api.ip.data5u.com/dynamic/get.html?order=bb925f3f5eb731be2b246a8b4e61fab3&sep=3"
	ipres = requests.get(url)
	if ipres.status_code != 200:
		time.sleep(2)
		return GetIp()
	return ipres.text.replace("\n","")



lock = threading.Lock()

class DbHelper(object):
	def __init__(self):
		self.redis = SaverRedis("35.220.199.242")
		self.mysql = MySQLdb.connect("35.220.199.242","root","123456","WenShuId" )
		self.mysql_cur = self.mysql.cursor()

	def exists_id(self,docid):
		sql = "select * from DocId where docid = '" +docid+"'"
		lock.acquire()
		try:
			self.mysql_cur.execute(sql)
			res = self.mysql_cur.fetchone()
		except:
			res = None
		lock.release()
		if res is None:
			return False
		return True

	def save_docid(self,docid):
		sql = "insert into DocId(docid) values('"+docid+"');"
		# print sql
		lock.acquire()
		try:
			self.mysql_cur.execute(sql)
			self.mysql.commit()
		except:
			self.mysql.rollback()
		lock.release()

dbh = DbHelper()




class DownloadThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)   
		self.proxies={
			"http":GetIp()
		}

	def download(self,docid):
		print(docid)
		if docid is None or len(docid)<20:
			return NotId
		if dbh.exists_id(docid):
			return ExistId
		url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID='+docid
		try:
			cont = requests.get(url,headers=ListHeaders,proxies=self.proxies,timeout=60)
		except Exception,e:
			print "request error"
			dbh.redis.save(docid)
			return DownError
		if len(cont.text)<500:
			print cont.text
		if cont.status_code == 200:
			f = open("Doc/"+docid+".js","w")
			f.write(cont.content)
			f.close()
			dbh.save_docid(docid)
		else:
			print cont
			# print cont.text
			print "download error"
			dbh.redis.save(docid)
			return DownError
			# exit()

	def run(self):
		while True:
			if self.download(dbh.redis.get_one()) == DownError:
				self.proxies["http"]=GetIp()



work = []

for i in range(10):
	w = DownloadThread()
	w.start()
	work.append(w)

for w in work:
	w.join()


