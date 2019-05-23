from flask import Flask
from flask import render_template
from mysql_db import *
import time,_thread
import json
from spider import *
from config import *
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/*')
db2 = MysqlDB({
    'host': DB_HOST,
    'port': DB_PORT,
    'user': USERNAME,
    'passwd': PASSWORD,
    'database': DB_NAME,
})



@app.route('/',methods=['POST','GET'])
def index():
	index_db = MysqlDB({
	    'host': DB_HOST,
	    'port': DB_PORT,
	    'user': USERNAME,
	    'passwd': PASSWORD,
	    'database': DB_NAME,
	})
	if request.method == 'POST':
		if request.form['action']=='delete':
			sql = "delete from productType where id = " + request.form['id']
			index_db.execute(sql)
			return 'ok'
		if request.form['action']=='add':
			name = request.form.get("name",'')
			print(name)
			if name=='':
				return '类型不可为空'
			if index_db.exitwithid('producttype','name',name):
				return "已经存在"
			# item={}
			# item['name'] = name
			# print(item)
			sql = 'insert into producttype(name) values("'+name+'")'
			print(sql)
			index_db.execute(sql)
			# index_db.insert('producttype',item)
			return 'ok'
		if request.form['action'] == 'do':
			name1 = request.form['type1']
			name2 = request.form['type2']
			id1 = request.form['id1']
			id2 = request.form['id2']
			index_db.update('productType',{'name':name1},'id',id2)
			index_db.update('productType',{'name':name2},'id',id1)
			return 'ok'
	columns = [
	# ["",'doup'],
	# ["",'dodown'],
	['职位列表', 'id'],
	['城市', 'state'],
	['行业', 'industry'],
	# ['删除','delete'],
	]
	sql = "select * from search_history"
	typeres = index_db.execute(sql)
	# for item in typeres:
	# 	item['delete'] = item['id']
		# sql = 'select count(*) from jobs where industry = "'+item['name']+'"'
		# typecount = index_db.execute(sql)
		# item['count'] = typecount[0]['count(*)']
	if len(typeres) == 0:
		typeres = []
	return render_template('allTypeProducts.html', columns=columns,datas=typeres)

@app.route('/type/<int:id>/')
def type_(id):
	index_db = MysqlDB({
	'host': DB_HOST,
	'port': DB_PORT,
	'user': USERNAME,
	'passwd': PASSWORD,
	'database': DB_NAME,
	})
	sql = "select state,industry from search_history where id = "+str(id)
	name = index_db.execute(sql)
	if len(name)==0:
		state = ''
	else:
		state = name[0]['state']
		industry = name[0]['industry']
	datasql = 'select * from jobs where state = "'+ state +'" and industry = "'+industry+'"'
	data = index_db.execute(datasql)
	# for d in data:
	# 	d['updateTime'] = d['updateTime'].strftime('%Y-%m-%d %H:%M:%S')
	# 	d['operation'] = d['productId']
	if len(data)==0:
		data = []
	return render_template('product.html',data = data, state=state,industry=industry)


@app.route('/update/')
def update_all():
	return start_update()

@app.route('/delProduct/',methods=['POST'])
def delProduct():
	index_db = MysqlDB({
	'host': DB_HOST,
	'port': DB_PORT,
	'user': USERNAME,
	'passwd': PASSWORD,
	'database': DB_NAME,
	})
	productId = request.form.get('productId','')
	if productId == '':
		return 'false'
	sql = 'delete from productView where productId = "'+productId+'"'
	index_db.execute(sql)
	return 'ok'

@app.route('/createspider/',methods=['POST'])
def add_url():
	global jobs_list_of_name,state
	index_db = MysqlDB({
	'host': DB_HOST,
	'port': DB_PORT,
	'user': USERNAME,
	'passwd': PASSWORD,
	'database': DB_NAME,
	})
	state_name = request.form.get('state','')
	# if state == '':
	# 	return 'url格式错误'
	# productId = re.compile('/(.*)\.html').findall(url)
	# if len(productId) == 0:
	# 	return 'url格式错误，获取不到productId'
	# pid = productId[0].split('/')[-1].split('_')[-1]
	# if index_db.exitwithid('productView','productId',pid):
	# 	return '已经存在此产品'
	industry = request.form.get('industry','')
	if state_name == "" or industry == '':
		print("state",state_name,"industry",industry)
		return "不允许输入为空"
	sql = "select count(*) from search_history where state = '"+state_name+"' and industry='"+industry+"'"
	count = index_db.execute(sql)
	count = count[0]['count(*)']
	if int(count) >0:
		return '已经存在此结果'
	if jobs_list_of_name.get(industry,None) == None:
		return '后台没有添加该行业'
	if state.get(state_name,None) == None:
		return '后台没有添加该城市'
	_thread.start_new_thread(spider,(state_name,industry))
	return 'ok'

@app.route('/exchangeItem/',methods=['POST'])
def exchangeItem():
	index_db = MysqlDB({
	'host': DB_HOST,
	'port': DB_PORT,
	'user': USERNAME,
	'passwd': PASSWORD,
	'database': DB_NAME,
	})
	source = request.form.get('source','')
	target = request.form.get('target','')
	if source == '' or target == '':
		return '非法访问'
	source = json.loads(source)
	source_id = source['pid']
	target = json.loads(target)
	target_id = target['pid']
	source['pid'] = target_id
	target['pid'] = source_id
	del source['operation']
	del target['operation']
	print(source)
	print(target)
	index_db.update('productView',source,'pid',source['pid'])
	index_db.update('productView',target,'pid',target['pid'])
	return 'ok'

@app.route('/ChangeTypeName/',methods=['POST'])
def ChangeTypeName():
	index_db = MysqlDB({
	'host': DB_HOST,
	'port': DB_PORT,
	'user': USERNAME,
	'passwd': PASSWORD,
	'database': DB_NAME,
	})
	old_type = request.form.get('oldtype','')
	new_type = request.form.get('newtype','')
	if new_type == '':
		return '类型不可为空'
	sql = 'select count(*) from producttype where name = "'+new_type+'"'
	print(sql)
	count_res = index_db.execute(sql)
	count = count_res[0]['count(*)']
	if count>0:
		return "已经存在此类型，修改失败！"
	sql = "update producttype set name = '"+new_type+"' where name = '"+old_type+"'"
	print(sql)
	index_db.execute(sql)
	sql = 'update productView set productType = "'+new_type+'" where productType = "'+old_type+'"'
	print(sql)
	index_db.execute(sql)
	return 'ok' 


if __name__ == '__main__':
    app.run(debug=True)