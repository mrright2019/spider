import __init__
from Config import *

import redis

class SaverRedis(object):

	def __init__(self,host="127.0.0.1",password="123456",port=6379):
		self.pool = redis.ConnectionPool(host=host,password=password,port=port)
		self.con = redis.Redis(connection_pool=self.pool)

	def save(self,docid,name="DocId"):
		self.con.lpush(name,docid)
		# pass

	def get_one(self):
		return self.con.lpop("DocId")


if __name__ == "__main__":
	s = SaverRedis()
	s.save("f06dcb7f-5cfc-4a62-9591-40807e2f29f2")
	print s.get_one()

