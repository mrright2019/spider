import requests
import re
import json,time

httpsession = requests.Session()
header = {
	'Host': 'video.acfun.cn',
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'Origin': 'http://www.acfun.cn',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	# 'Accept': '*/*',
	# 'Referer': 'http://www.acfun.cn/v/ac4930768',
	# 'Accept-Encoding': 'gzip, deflate',
	# 'Accept-Language': 'en-US,en;q=0.9',
}

def run(url):
	res = httpsession.get(url)
	print(res)
	# print(res.text)
	vid = re.findall(',"videoId":(.*?),',res.text)
	print(vid[0])
	getMasterList(vid[0])

def getVideo(vid):
	url = 'http://www.acfun.cn/video/getVideo.aspx?id='+vid
	res = httpsession.get(url)
	if res.status_code!=200:
		print("获取视频信息失败")
		return
	json_data = json.loads(res.text)
	print(json_data)

def getMasterList(vid):
	url = 'http://www.acfun.cn/video/getVideo.aspx?id='+vid
	res = httpsession.get(url)
	if res.status_code!=200:
		print("获取视频信息失败")
		return
	json_data = json.loads(res.text)
	print(json_data)
	masterurl = 'http://www.acfun.cn/rest/pc-direct/video/hlsMasterPlayList?vid='+json_data['sourceId']+'&ct=85&ev=3&sign='+json_data['encode']+'&time='+str(int(time.time()*1000))
	print('masterurl:',masterurl)
	res = httpsession.get(masterurl)
	route_url = [ x  for x in res.text.split("\n") if len(x)!=0 and x[0]!='#']
	f = open(vid+'.flv','wb')
	# f.close()
	for route in route_url:
		print("route",route)
		res= httpsession.get(route)
		part_url = [ x for x in res.text.split('\n') if len(x)!=0 and x[0]!='#']
		for part in part_url:
			print("正在下载part:",part)
			download_vider_part(part,f)
		f.close()
		return


def download_vider_part(url, f):
	r = httpsession.get(url, stream=True)
	print(r.status_code)
	for chunk in r.iter_content(1024 * 100):
		f.write(chunk)
run('http://www.acfun.cn/v/ac4950678')

