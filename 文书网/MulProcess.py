#coding:utf8

# from multiprocessing import Pool,Lock,Process,JoinableQueue
import time
# import multiprocessing
from main import *
import os
import Queue
from Saver import *


import threading
lock = threading.Lock()


ipqueue = Queue.Queue()
getting=False


def GetIp():
	getting = True
	url = "http://api.ip.data5u.com/dynamic/get.html?order=bb925f3f5eb731be2b246a8b4e61fab3&sep=3"
	ipres = requests.get(url)
	if ipres.status_code != 200:
		time.sleep(2)
		return GetIp()
	return ipres.text.replace("\n","")





def GetInter(day1,day2):
	d1 = datetime.datetime.strptime(day1, '%Y-%m-%d')
	d2 = datetime.datetime.strptime(day2 ,'%Y-%m-%d')
	return (d1-d2).days


def changeip(proxies):
	proxies["http"] = GetIp()




DateQueue = Queue.Queue()

hasspideingday = [day for day in open("log/days","r").read().split("\n")]

date = "2016-01-19"
while GetInter("2017-01-01",date) >0:
	date = getday(date,2)
	if date in hasspideingday:
		continue
	DateQueue.put(date)


class  MyThread(threading.Thread):
	def  __init__(self,name):   
	    threading.Thread.__init__(self)   
	    self.proxies = {
	    	"http":None
	    }

	def run(self):   
		global lock,DateQueue
		s = requests.session()
		s.keep_alive = False
		while True:
			lock.acquire()
			if DateQueue.empty():
				lock.release()
				return
			date = DateQueue.get()
			lock.release()
			enddate = getday(date,1)
			page = 1
			while page<=20:
				print(date,page)
				result = GetContentByDay(date,enddate,page=page,proxies =self.proxies ,s =s)
				print(date,page)
				# if result == NextIp:
				# 	changeip(self.proxies)
				if result == RemindKey:
					continue
				elif result == NoNext:
					page =100
				elif result == HaveNext:
					page+=1
			f = open("log/days","a+")
			f.write(date+"\n")
			f.close()


if __name__ == '__main__':
	work_list = []
	# print DateQueue.qsize()
	loop = 15 if DateQueue.qsize() > 15  else DateQueue.qsize()
	print loop
	for i in range(1):
		t = MyThread(i)
		t.start()
		work_list.append(t)
	for t in work_list:
		t.join()