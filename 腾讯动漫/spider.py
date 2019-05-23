import requests
import json
import time
import re,csv,os
from bs4 import BeautifulSoup
listurl = 'https://v.qq.com/x/bu/pagesheet/list?append=1&channel=cartoon&iarea=1&listpage=3&offset=48&pagesize=24&sort=18'
headers = {
	# GET https://video.coral.qq.com/varticle/3129219563/comment/v2?callback=_varticle3129219563commentv2&orinum=10&oriorder=o&pageflag=1&cursor=6462898130325965940&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=1549191673993 HTTP/1.1
'Host': 'video.coral.qq.com',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'Accept': '*/*',
'Referer': 'https://page.coral.qq.com/coralpage/comment/video.html',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9',
'Cookie': 'pgv_pvi=5146876928; RK=efjRvzfN35; ptcz=46c62d6d8d937d80601fd6bd216c67e57e8b359f79969114ae9de72b20e6ec1a; tvfe_boss_uuid=0465d32789561d41; pgv_pvid=3373793510; pgv_info=ssid=s3518098712; g_tk=642fba8ac52e1239c4655e48dc6a645b641dae73',
}
def get_id(url,retry=0):
	if retry>=3:
		return None
	res=requests.get(url,verify=False)
	# print(res.text)
	comid =	re.findall('"comment_id":"(.*?)",', res.text)
	if len(comid)==0:
		return get_id(url,retry+1)
	return comid[0]

def write_to_scv(filename,replies):
	out = open(filename,'a',encoding='utf8',newline='')
	#设定写入模式
	csv_write = csv.writer(out,dialect='excel')
	for reply in replies:
		item = [reply]
		csv_write.writerow(item)
	out.close()


def get_reply(comid,title=''):
	if os.path.exists('data/'+title+'.csv'):
		return
	replies = []
	time_ = int(float(time.time())*1000)
	callback = '_varticle'+comid+'commentv2'
	reply_num = 0
	comurl = 'https://video.coral.qq.com/varticle/'+comid+'/comment/v2?callback='+callback+'&orinum=10&oriorder=o&pageflag=1&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_='+str(time_)
	print(comurl)
	res = requests.get(comurl,headers=headers,verify=False)
	json_str = res.content.decode('utf-8')
	json_str = json_str.replace(callback+'(','')
	json_str = json_str[:-1]
	# print(json_str)
	json_data = json.loads(json_str)
	last_cursor = json_data['data']['first']
	while reply_num <100:
		time_ = int(float(time.time())*1000)
		reply_url = 'https://video.coral.qq.com/varticle/'+comid+'/comment/v2?callback='+callback+'&orinum=10&oriorder=o&pageflag=1&cursor='+last_cursor+'&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_='+str(time_)
		res = requests.get(reply_url,headers=headers,verify=False)
		json_str = res.content.decode('utf-8')
		json_str = json_str.replace(callback+'(','')
		json_str = json_str[:-1]
		json_data = json.loads(json_str)
		last_cursor = json_data['data']['last']
		print('last_cursor:',last_cursor)
		if not last_cursor:
			break
		for reply in json_data['data']['oriCommList']:
			print(reply['content'])
			replies.append(reply['content'])
			reply_num+=1
	write_to_scv('data/'+title+'.csv',replies)

avnum = 0
def spider_page_list(page):
	global avnum
	listurl = 'https://v.qq.com/x/bu/pagesheet/list?append=1&channel=cartoon&iarea=1&listpage='+str(page)+'&offset='+str(page*24)+'&pagesize=24&sort=18'
	res = requests.get(listurl,verify=False)
	# print(res.content.decode("utf-8"))
	soup = BeautifulSoup(res.content.decode("utf-8"),features="lxml")
	a_list = soup.find_all('a',attrs={'class':'figure'})
	for a in a_list:
		print(a.attrs['title'])
		link = a.attrs['href']
		print(link)
		comid = get_id(link)
		if comid == None:
			continue
		print(comid)
		get_reply(comid,a.attrs['title'])
		if avnum>200:
			exit()
		avnum+=1




pn = 1
while avnum<200:
	spider_page_list(pn)
	pn+=1
exit(0)
