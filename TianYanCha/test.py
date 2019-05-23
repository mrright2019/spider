#coding:utf-8
import requests
from bs4 import BeautifulSoup
# from encryfun import *
from ttf_decrypt import *
headers = {
	'Host': 'www.tianyancha.com',
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

headers2 = {
"Host": "www.tianyancha.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Cookie": "TYCID=16ccaba0dfca11e8b9d0b3741fb487de; undefined=16ccaba0dfca11e8b9d0b3741fb487de; ssuid=9461596208; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1542437216,1542624006,1542633154,1542633208; _ga=GA1.2.1940698707.1541291851; RTYCID=d4a3c2a315ed4704a189907b697ba553; CT_TYCID=911babecceca438393c18e77e8967673; _gid=GA1.2.1339462310.1542624014; _gat_gtag_UA_123487620_1=1; tyc-user-info=%257B%2522myQuestionCount%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25226%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzg2NTMxMzM4NSIsImlhdCI6MTU0MjYzMzE5NywiZXhwIjoxNTU4MTg1MTk3fQ.CkySHsSNw_vghasknSDMsQRqa6vkef4v2kLbdKQ5N_9veXBUznzuAAeBVHlE1AYpFfbTpsHJf9zMPMXGE_sfEA%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217865313385%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzg2NTMxMzM4NSIsImlhdCI6MTU0MjYzMzE5NywiZXhwIjoxNTU4MTg1MTk3fQ.CkySHsSNw_vghasknSDMsQRqa6vkef4v2kLbdKQ5N_9veXBUznzuAAeBVHlE1AYpFfbTpsHJf9zMPMXGE_sfEA; aliyungf_tc=AQAAADCeJCjZqgkA+RrAeDvUImHn1AQ7; csrfToken=5_9tDl3X4ynyXnLul-nvUBRD; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1542633208",
"Upgrade-Insecure-Requests": "1",
"Cache-Control": "max-age=0",
}



s = requests.session()
s.keep_alive = False

import hashlib

def md5(s):
	md5 = hashlib.md5(s.encode('utf-8')).hexdigest()
	return md5


p = s.get("https://www.tianyancha.com",headers=headers2)
cookies = p.cookies
# print p.content
keyword = "阿里"
search_url = "https://www.tianyancha.com/search"
endparams = "?key=%E9%98%BF%E9%87%8C&base=bj&areaCode=110101"


def download_ttf():
	url = "https://static.tianyancha.com/fonts-styles/fonts/66/66541369/tyc-num.ttf"
	ttfres = requests.get(url)
	if ttfres.status_code ==200:
		ttfmd5 = md5(ttfres.text)
		f = open("TTF/"+ttfmd5+".ttf","wb")
		f.write(ttfres.content)
		return "TTF/"+ttfmd5+".ttf"






for i in range(1,6):
	if i == 1:
		page_str = ""
		# continue
	else:
		page_str = "/p"+str(i)
	list_url = search_url+page_str+endparams
	# print list_url
	list_response = s.get(list_url,headers=headers2,cookies = cookies)
	cookies = list_response.cookies
	# print list_response
	# print list_response.content
	soup = BeautifulSoup(list_response.content,'html.parser')
	all_a = soup.find_all('a',attrs={"tyc-event-ch":"CompanySearch.Company"})
	ttfname = download_ttf()
	print ttfname
	t = ttf(ttfname,corn = "baidu")
	# print all_a
	for a in all_a:
		print a["href"]
		more = s.get(a["href"],headers=headers2,cookies=cookies)
		# print [more.content
		# print more.content
		content_soup = BeautifulSoup(more.content,"html.parser")
		# print content_soup.title
		hidetext = content_soup.find("text",attrs={"class":"tyc-num"})
		if hidetext is None:
			continue
		text = hidetext.get_text()
		# print type(text)
		print text
		detext = ""
		for t_ in text:
			# print t_
			detext += t.decrypt(str(t_))
		print detext
		exit()