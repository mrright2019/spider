from config import *
import time
from sendmail import *



def getmonth(month):
	m = {
		'Jan':'01','Feb':'02','Mar':'03','Apr':'04',
		'May':'05','Jun':'06','Jul':'07','Ang':'08',
		'Sep':'09','Oct':'10','Nov':'11','Dec':'12',
	}
	return m.get(month,'')

def get_last_id():
	sql = 'select * from tweepy where retweeted=0  order by id desc limit 1'
	last_db_t = global_db.execute(sql)
	if len(last_db_t) == 0:
		last_tweepy = api.search(q=searchQuery,count=50,until=untilId)
		tweet = last_tweepy[0]
		print(tweet.created_at)
		print(tweet.user.id_str)
		return tweet.id_str
	else:
		return last_db_t[0]['tweepy_id']

def is_exists(id):
	res = global_db.exitwithid('tweepy','tweepy_id',id)
	if res==0:
		return False
	return True

max_id = get_last_id()
print(max_id)
# tweepys = api.search(q=searchQuery,until=untilId)
# print(tweepys)
# exit()
def get_this_rt(id):
	tweepys = api.retweets(id,100 )
	print(tweepys)
	for tweet in tweepys:
		item = {}
		item['tweepy_id'] = tweet.id_str
		item['text'] = tweet.text
		item['create_at'] = tweet.created_at
		item['user_id'] = tweet.user.id_str
		item['retweet_count'] = tweet.retweet_count
		item['favorite_count'] = tweet.favorite_count
		try:
			item['retweeted_id'] = tweet.retweeted_status.id_str
			item['retweeted'] = 1
		except:
			item['retweeted'] = 0
		item['hashtags'] = ''
		for tag in tweet.entities['hashtags']:
			item['hashtags'] = item['hashtags']+'#'+tag['text']
		if is_exists(item['tweepy_id']):
			log('已经存在item:',item)
			continue
		log('插入rt item:',item)
		global_db.insert('tweepy',item)
		if item['retweet_count']>0:
			get_this_rt(item['tweepy_id'])

def get_once_media_by_api():
	global next_bid
	json_data = search_by_inm(searchQuery,'201101010000','201201010000',next=next_bid)
	for tweet in json_data['results']:
		print(tweet)
	exit()
	global max_id
	# help(api.search)
	# return
	new_tweets = api.search(q=searchQuery,count=100,
	                max_id=max_id)
	for tweet in new_tweets:
		item = {}
		item['tweepy_id'] = tweet.id_str
		item['text'] = tweet.text
		item['create_at'] = tweet.created_at
		if sinceId in str(tweet.created_at):
			sendmail("760737729@qq.com")
			exit()
		item['user_id'] = tweet.user.id_str
		item['retweet_count'] = tweet.retweet_count
		item['favorite_count'] = tweet.favorite_count
		try:
			item['retweeted_id'] = tweet.retweeted_status.id_str
			item['retweeted'] = 1
		except:
			item['retweeted'] = 0
		item['hashtags'] = ''
		for tag in tweet.entities['hashtags']:
			item['hashtags'] = item['hashtags']+'#'+tag['text']
		if is_exists(item['tweepy_id']):
			log('已经存在item:',item)
			continue
		log('插入item:',item)
		global_db.insert('tweepy',item)
		if item['retweet_count']>0:
			get_this_rt(item['tweepy_id'])
		max_id = item['tweepy_id']

get_once_media_by_api()
exit()
while True:
	try:
		get_once_media_by_api()
	except Exception as e:
		log(e)
		time.sleep(3)
		exit()