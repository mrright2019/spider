import requests
import json
from config import *
from bs4 import BeautifulSoup
state_name = '北京'
job_name = '互联网IT'


def spider(state_name,job_name):
	global db
	db.insert("search_history",{'state':state_name,'industry':job_name})
	job_list = jobs_list_of_name[job_name]
	for job in job_list:
		url = 'https://sou.zhaopin.com/?jl='+str(state[state_name])+'&kw='+job+'&kt=3'
		pg = 1
		for pg in range(1,12):
			response = requests.get('https://fe-api.zhaopin.com/c/i/sou?start='+str(pg*90)+'&pageSize=90&cityId=736&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw='+job+'&kt=3&_v=0.90415108')
			print(len(response.text))
			jsondata = json.loads(response.text)
			if jsondata.get('data',None) == None:
				continue
			for res in jsondata['data']['results']:
				item = {}
				item['salary']=res['salary']
				item['jobName'] = res['jobName']
				item['positionURL'] = res['positionURL']
				item['workingExp'] = res['workingExp']['name']
				item['company'] = res['company']['name']
				item['industry'] = job_name
				item['state'] = state_name
				item['type'] = res['company']['type']['name']
				item['size'] = res['company']['size']['name']
				db.insert("jobs",item)
				print("插入数据",item)
		# exit()


# spider(state_name,job_name)