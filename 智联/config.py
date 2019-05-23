from mysql_db import *
import threading
global_lock = threading.Lock()



DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'job_spider'
TB_NAME = 'search_history'
USERNAME = 'root'
PASSWORD = ''



db = MysqlDB({
    'host': DB_HOST,
    'port': DB_PORT,
    'user': USERNAME,
    'passwd': PASSWORD,
    'database': DB_NAME,
})


jobs_list_of_name = {}

jobs_list_of_name['互联网IT'] = [
	"Java开发",
	"UI设计师",
	"PHP",
	"Web前端",
	"Python",
	"美工",
	"算法工程师",
	"深度学习",
	"Android",
	"Hadoop",
	"Node.js",
	"数据分析师",
	"人工智能",
	"区块链电气工程师",
	"数据架构",
	"数据开发",
	"电子工程师",
	"测试工程师",
	"硬件工程师",
	"设备工程师",
	"结构工程师",
	"淘宝运营",
	"产品助理",
	"淘宝客服",
	"金融",
	"游戏运营",
	"产品运营",
	"天猫运营",
	"运营专员",
	"工艺工程师",
	"产品经理",
	"新媒体运营",
]

state ={}
state['全国']=489
state['北京']=530
state['上海']=539
state['郑州']=719
state['西安']=854
state['沈阳']=599
state['苏州']=630
state['青岛']=703
state['济南']=702
state['南京']=635
state['长春']=613
state['大连']=600
state['武汉']=736
state['杭州']=653
state['成都']=801
state['天津']=531
state['广州']=763
state['深圳']=765
