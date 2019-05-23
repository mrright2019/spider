import redis
App_Path = "D:/Work/WenShuCourt/"

headers = {
	'Host': 'wenshu.court.gov.cn',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate',
	'Referer': 'http://wenshu.court.gov.cn/',
	# 'Cookie': 'Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1540191393; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1540191419; _gscu_2116842793=40191393rrdes020; _gscs_2116842793=40191393plsnhv20|pv:2; _gscbrs_2116842793=1; vjkl5=7ef92d099ff909a7001231889c8ae52fa903c376',
	# 'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
	'Cache-Control': 'max-age=0',
	'Connection': 'close',
}

ListHeaders={
	'Host': 'wenshu.court.gov.cn',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
	'Accept': '*/*',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate',
	'Referer': 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=ZGG62AZJ&guid=1cc25cc2-d082-68677b06-2bf53e1d5cff&conditions=searchWord+1+WSLX++%E6%96%87%E4%B9%A6%E7%B1%BB%E5%9E%8B:%E5%88%A4%E5%86%B3%E4%B9%A6',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-Requested-With': 'XMLHttpRequest',
	# 'Content-Length': '228',
	'Connection': 'close',
	'Cache-Control': 'max-age=0',
}


pool = redis.ConnectionPool(host="localhost",password="123456",port=6379)
con = redis.Redis(connection_pool=pool)

