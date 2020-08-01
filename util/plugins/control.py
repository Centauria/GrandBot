# -*- coding: utf-8 -*-
import util.db.mongodb.operation as op
from util.base.singleton import Singleton
from util import configuration, reload_config
from .blacklist import Blacklist


@Singleton
class PluginControl(object):

	def __init__(self):
		# 初始化关键字数组
		self.keywords = configuration.keywords
		# 初始化黑名单类
		self.blacklist = Blacklist()

	def refresh(self):
		configuration = reload_config()
		self.keywords = configuration.keywords

	def authority(self, fromUserId):
		# 用户权限判断
		if fromUserId not in configuration.admin:
			return False
		return True

	def add(self, new_plugin, fromGroupId):
		if not op.count_group_plugins(new_plugin, fromGroupId):
			result = op.insert_group_plugins(new_plugin, fromGroupId)
			if result.inserted_id:
				print(f"plugin:{new_plugin} in Group Id : {fromGroupId} has been opened!")
				return {"result": True, "content": "插件 : " + new_plugin + " 打开成功"}
			else:
				return {"result": False, "content": "插件 : " + new_plugin + " 打开失败"}
		else:
			print(f"plugin:{new_plugin} in Group Id : {fromGroupId} is already opened!")
			return {"result": False, "content": "插件 : " + new_plugin + " 已处于开启状态"}

	def delete(self, plugin, fromGroupId):
		result = op.delete_group_plugins(plugin, fromGroupId)
		if result['ok'] and result['n'] != 0:
			print(f"plugin:{plugin} in Group Id : {fromGroupId} delete successfully!")
			return {"result": True, "content": "插件 : " + plugin + " 关闭成功"}
		elif result['ok'] and result['n'] == 0:
			return {"result": False, "content": "插件 : " + plugin + " 未开启"}
		else:
			return {"result": False, "content": "插件 : " + plugin + " 关闭失败"}

	def update(self, plugin, fromGroupId, para):
		return op.update_group_plugins(plugin, fromGroupId, para)

	def add_all(self, fromGroupId):
		add_false = []

		for plugin in self.keywords:

			if not op.count_group_plugins(plugin, fromGroupId):
				result = op.insert_group_plugins(plugin, fromGroupId)
				if result.inserted_id:
					print(f"plugin:{plugin} in Group Id : {fromGroupId} has been opened!")
				else:
					add_false.append(plugin)

		return add_false

	def delete_all(self, fromGroupId):
		delete_false = []

		for plugin in self.keywords:
			result = op.delete_group_plugins(plugin, fromGroupId)
			if result['ok'] and result['n'] != 0:
				print(f"plugin:{plugin} in Group Id : {fromGroupId} delete successfully!")
			elif not result['ok']:
				delete_false.append(plugin)

		return delete_false

	def find_all(self, fromGroupId):
		results = op.find_group_plugins(fromGroupId)
		collections = []
		for result in results:
			collections.append(result)
		return collections

	def find_one(self, plugin, fromGroupId):
		result = op.find_one_group_plugins(plugin, fromGroupId)
		return result

	def check(self, plugin, fromUserId, fromGroupId):

		# plugin检测
		result_plugin = op.find_one_group_plugins(plugin, fromGroupId)

		# blacklist检测
		result_blacklist = self.blacklist.check(int(fromUserId), int(fromGroupId))

		if result_plugin and not result_blacklist:
			return True
		else:
			return False

	def is_command(self, command, fromGroupId):
		for key in self.keywords:
			if command == key:
				return True
		if command == "plugins":
			return True
		if command[0] == '.':
			return True
		return False
