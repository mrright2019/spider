
import os
import tweepy
import time,json
import sys
from datetime import datetime
import requests
from mysql_db import *
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'tweets'
USERNAME = 'root'
PASSWORD = ''



global_db = MysqlDB({
    'host': DB_HOST,
    'port': DB_PORT,
    'user': USERNAME,
    'passwd': PASSWORD,
    'database': DB_NAME,
})

callbackurl = 'www.beijingdaxingtahoecn.top/callback';
API_KEY = 'RxmyG9g68xY6lIdqudK0nbwpy'
API_SECRET = 'HZ6sDqsqRgLFLP1vB811AM5kdi6iixNdTWIY25cVp2vBSac5JI'
debug = True


def log(v,*args,**argv):
	if debug:
		print(v,*args,**argv)

auth = tweepy.auth.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token('1087104883449360390-y2FJrReQCefxnLgp32eXdkdcFqqWgV', 'kx6TnywbMmocRcxcB3IYwlSFmgQ5kCqAbSI0z9jNcdljR')

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)


searchQuery = "world"

sinceId = '2019-02-12'
untilId = '2018-02-27'


bk = 'AAAAAAAAAAAAAAAAAAAAAPhn9QAAAAAAVCX8riz1kt0%2BcSnmR3MP8npR6WU%3DaYQGGfST0q4ZaZO0gKzggcxJxf2nqrdltGc8yypS8TLJFEncUV'


btheader = {
	"Authorization":"Bearer "+bk,
}

fromDate='201101010000'
toDate='201201010000'
next_bid=None


def search_by_inm(keyword,fromDate,toDate,next=None):
	url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/Dev1.json?query='+keyword+'&maxResults=500&fromDate='+fromDate+'&toDate='+toDate#+'&next=eyJhdXRoZW50aWNpdHkiOiJmY2U0MDViZGY0MTI4YzAzZmRkNDg3Mjg4MmVlODZhNWI3YWMwMGZkYWJjYjg1MWI0MjBlMmE1NmZkMjU5YjVkIiwiZnJvbURhdGUiOiIyMDExMDEwMTIzMTUiLCJ0b0RhdGUiOiIyMDEyMDEwMTIzMTUiLCJuZXh0IjoiMjAxMjAxMDEyMzA5NDktMTUzNjEzOTI5Njc3OTk2MDMxLTAifQ=='
	if next:
		url = url+'&next='+next
	res = requests.get(url,headers=btheader)
	# log(res.text)
	return json.loads(res.text)


# print(search_by_inm(searchQuery,'201101010000','201201010000',next=_next))