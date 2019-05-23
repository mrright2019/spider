import requests,json,time
from bs4 import BeautifulSoup
import csv
pageurl = 'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&is_finish=-1&copyright=-1&season_status=-1&pub_date=-1&style_id=-1&order=3&st=4&sort=0&season_type=4&pagesize=20&page='
avnum = 0
headers = {
	'Host': 'bangumi.bilibili.com',
	'Connection': 'keep-alive',
	'Accept': 'application/json, text/plain, */*',
	'Origin': 'https://www.bilibili.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	'Referer': 'https://www.bilibili.com/guochuang/index/?spm_id_from=333.113.b_7375626e6176.7',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Cookie': 'buvid3=CCB9A5F4-EF8D-469F-93E3-A90E5DCD163148785infoc; LIVE_BUVID=AUTO3815491743297270; stardustvideo=1; CURRENT_FNVAL=16; sid=9593y49g; fts=1549185606',
}
oidheaders = {
	'Host': 'www.bilibili.com',
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Referer': 'https://www.bilibili.com/guochuang/index/?spm_id_from=333.113.b_7375626e6176.7',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Cookie': '_uuid=6EEC8F41-FD48-BB4B-CB6F-A3460B16E30626065infoc; buvid3=CCB9A5F4-EF8D-469F-93E3-A90E5DCD163148785infoc; LIVE_BUVID=AUTO3815491743297270; stardustvideo=1; CURRENT_FNVAL=16; fts=1549185606; sid=m5k0ymez',
}
plheaders = {
	# GET https://api.bilibili.com/x/v2/reply?callback=jQuery172021906124252505754_1549186694326&jsonp=jsonp&pn=1&type=1&oid=2477032&sort=0&_=1549187530455 HTTP/1.1
	'Host': 'api.bilibili.com',
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	'Accept': '*/*',
	'Referer': 'https://www.bilibili.com/bangumi/play/ss2543/',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Cookie': 'buvid3=CCB9A5F4-EF8D-469F-93E3-A90E5DCD163148785infoc; LIVE_BUVID=AUTO3815491743297270; stardustvideo=1; CURRENT_FNVAL=16; fts=1549185606; sid=m5k0ymez',
}
def get_page_list(page):
	global avnum
	url = pageurl+str(page)
	res = requests.get(url,headers=headers, verify=False)
	json_data = json.loads(res.text)
	link = json_data['result']['data'][0]['link']
	for data in json_data['result']['data']:
		print(data['title'])
		oid = getoid(link)
		print(oid)
		get_reply(oid,data['title'])
		avnum+=1
		if avnum>=200:
			exit()

def get_reply(oid,title):
	time_ = int(float(time.time())*1000)
	# plurl = 'https://api.bilibili.com/x/v2/reply?callback=jQuery172021906124252505754_1549186694326&jsonp=jsonp&pn=2&type=1&oid='+oid+'&sort=2&_='+str(time_)
	plnum = 0
	pn = 1
	replies = []
	while plnum<100:
		plurl = 'https://api.bilibili.com/x/v2/reply?callback=jQuery172021906124252505754_1549186694326&jsonp=jsonp&pn='+str(pn)+'&type=1&oid='+oid+'&sort=2&_='+str(time_)
		res = requests.get(plurl,headers=plheaders,verify=False)
		json_data = json.loads(res.content[42:-1])
		if len(json_data['data']['replies']) == 0:
			break
		for reply in json_data['data']['replies']:
			print(reply['content']['message'])
			replies.append(reply['content']['message'])
			plnum+=1
		pn = pn+1
	write_to_scv('data/'+title+'.csv',replies)

def write_to_scv(filename,replies):
	out = open(filename,'a',encoding='utf8',newline='')
	#设定写入模式
	csv_write = csv.writer(out,dialect='excel')
	for reply in replies:
		item = [reply]
		csv_write.writerow(item)
	out.close()

def getoid(url):
	res = requests.get(url,headers=oidheaders,verify=False)
	# print(res.text)
	soup = BeautifulSoup(res.content,features="lxml")
	text = soup.find('a',attrs={'class':'info-sec-av'})#('//*[@id="bangumi_header"]/div[1]/div[1]/a[2]')
	return text.text[2:]

pagenum = 1
while True:
	get_page_list(pagenum)
	pagenum+=1

#GET /x/v2/reply?callback=jQuery17204879273679366569_1549186271256&jsonp=jsonp&pn=2&type=1&oid=2477032&sort=0&_=1549186294736 HTTP/1.1
#GET /x/v2/reply?callback=jQuery172003754868949511603_1549186342809&jsonp=jsonp&pn=2&type=1&oid=9659814&sort=2&_=1549186378239 HTTP/1.1