# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration
from util.plugins.control import PluginControl
from .action_in_type import action_in_type
import json


def admin_plugins_group(ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_plugins(1, ctx.Content, ctx.FromGroupId)


# plugins管理
def admin_plugins(flag, content, fromId):
	content = content.lstrip('.')
	if content.split(' ', 1)[0] == 'plugins':
		commands = content.split(' ')

		plugins = PluginControl()

		# open命令
		if len(commands) == 3 and commands[1] == "open":

			if commands[2] in plugins.keywords:
				res = plugins.add(commands[2], fromId)
				return action_in_type(fromId, res["content"], flag, res["result"])
			elif commands[2] == "all":
				false_set = plugins.add_all(fromId)
				if false_set == []:
					return action_in_type(fromId, "插件全部开启成功", flag, True)
				else:
					content = "插件 "
					for plugin in false_set:
						content += plugin + " , "
					content += "开启失败"
					return action_in_type(fromId, content, flag, False)
			else:
				return action_in_type(fromId, commands[2] + "不是可开启的插件", flag, False)

		# close命令
		elif len(commands) == 3 and commands[1] == "close":

			if commands[2] == "all":
				false_set = plugins.delete_all(fromId)
				if false_set == []:
					return action_in_type(fromId, "插件全部关闭成功", flag, True)
				else:
					content = "插件 "
					for plugin in false_set:
						content += plugin + " , "
					content += "关闭失败"
					return action_in_type(fromId, content, flag, False)
			else:
				res = plugins.delete(commands[2], fromId)
				return action_in_type(fromId, res["content"], flag, res["result"])

		# list命令
		elif len(commands) == 2 and commands[1] == "list":

			results = plugins.find_all(fromId)

			content = "插件列表：\n"
			for key in plugins.keywords:
				new_flag = 0
				for result in results:
					if key == result["plugin"]:
						new_flag = 1
				is_opened = '(√) ' if new_flag else '(×) '
				content += is_opened + key + "\n"

			return action_in_type(fromId, content, flag, False)




def admin_plugins_find(GroupId: int, page: int, page_size: int):
	plugins = PluginControl()
	list = plugins.find_all(GroupId)
	all_list = []

	with open("res/json/plugins_para.json", 'r') as load_file:
		plugins_content = json.load(load_file)

	id = 1
	keywords = plugins.keywords
	for keyword in keywords:
		flag = 0
		for plugin in list:
			if plugin["plugin"] == keyword:
				plugin.pop("_id")
				plugin["id"] = id
				plugin["opened"] = True
				if "param" not in plugin:
					plugin["param"] = {}
				all_list.append(plugin)
				flag = 1
				break
		if not flag:
			if plugins_content[keyword]:
				param = plugins_content[keyword]
			else:
				param ={}
			plugin = {"id": id, "plugin": keyword, "opened": False, "param": param, "from_group_id": GroupId}
			all_list.append(plugin)
		id += 1

	if len(all_list) == 0:
		return {"result": False, "content": {}}

	start = (page - 1) * page_size
	end = min(page * page_size, len(all_list))

	return {"result": True, "content": all_list[start:end]}
