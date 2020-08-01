# -*- coding: utf-8 -*-
import time
import util.db.mongodb.operation as op
from util.base.singleton import Singleton


@Singleton
class Blacklist(object):

	def __init__(self):
		pass

	# 判断是否在黑名单
	def check(self, userId: int, groupId: int):
		result = op.find_one_group_blacklist(userId, groupId)
		if not result:
			return False
		if int(time.time()) >= result["start_time"] + result["interval"]:
			self.delete(userId, groupId)
			return False
		return True

	# 增加黑名单
	def add(self, userId: int, groupId: int, interval, srartTime):
		if op.count_group_blacklist(userId, groupId):
			op.delete_group_blacklist(userId, groupId)

		result = op.insert_group_blacklist(userId, groupId, interval, srartTime)
		return result

	# 删除黑名单
	def delete(self, userId: int, groupId: int):
		result = op.delete_group_blacklist(userId, groupId)
		if result['ok'] and result['n'] != 0:
			return True
		elif result['ok'] and result['n'] == 0:
			return False
		else:
			return False

	def find_all(self, groupId: int):
		results = op.find_group_blacklist(groupId)
		collections = []
		for result in results:
			collections.append(result)
		return collections
