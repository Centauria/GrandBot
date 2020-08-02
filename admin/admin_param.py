# -*- coding: utf-8 -*-
import json
from iotbot import GroupMsg
from util import configuration
from util.plugins.control import PluginControl
from .action_in_type import action_in_type


def admin_param_group(ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_param(1, ctx.Content, ctx.FromGroupId)


def admin_param(flag, content, fromId):
	content = content.lstrip('.')

	if content.split(' ', 1)[0] == 'param':
		command = content.split(' ')

		if len(command) == 4:
			# 允许的参数列表
			with open("res/json/plugins_para.json", "r") as load_file:
				json_content = json.load(load_file)

			# 命令的插件、参数允许
			if command[1] not in json_content:
				return action_in_type(fromId, "插件未开启", flag, False)
			if command[2] not in json_content[command[1]]:
				return action_in_type(fromId, "参数不存在", flag, False)

			key = "param." + command[2]
			para = {"$set": {key: command[3]}}

			plugins = PluginControl()
			result = plugins.update(command[1], fromId, para)
			if not result["ok"] or not result["nModified"]:
				return action_in_type(fromId, "参数更新失败", flag, False)

			return action_in_type(fromId, "参数更新成功", flag, True)

		else:
			return action_in_type(fromId, "命令格式错误", flag, False)


def admin_param_find(GroupId: int, page: int, page_size: int):
	plugins = PluginControl()
	list = plugins.find_all(GroupId)

	id = 1
	for plugin in list:
		plugin.pop("_id")
		plugin["id"] = id
		id += 1

	if len(list) == 0:
		return {"result": False, "content": {}}

	start = (page - 1) * page_size
	end = min(page * page_size, len(list))
	return {"result": True, "content": list[start:end]}
