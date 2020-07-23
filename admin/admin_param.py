# -*- coding: utf-8 -*-
import json
from iotbot import GroupMsg, Action
from util import configuration
from util.plugins.control import PluginControl


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
				action_in_type(fromId, "插件未开启", flag)
				return
			if command[2] not in json_content[command[1]]:
				action_in_type(fromId, "参数不存在", flag)
				return

			key = "param." + command[2]
			para = {"$set": {key: command[3]}}

			plugins = PluginControl()
			result = plugins.update(command[1], fromId, para)
			if not result["ok"] or not result["nModified"]:
				action_in_type(fromId, "参数更新失败", flag)
				return

			action_in_type(fromId, "参数更新成功", flag)

		else:
			action_in_type(fromId, "命令格式错误", flag)


def action_in_type(fromId, content, flag):
	if flag == 1:
		action = Action(configuration.qq)
		return action.send_group_text_msg(fromId, content)
	else:
		return fromId, content
