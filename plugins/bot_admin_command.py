# -*- coding: utf-8 -*-
import time
import json
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration
from util.plugins.control import PluginControl


def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		content = ctx.Content.lstrip('.')
		action = Action(configuration.qq)
		plugins = PluginControl()

		if content.split(' ', 1)[0] == 'blacklist':
			command = content.split(' ')
			if len(command) == 3 and command[1] == "remove":
				if plugins.blacklist.delete(int(command[2]), ctx.FromGroupId):
					action.send_group_text_msg(ctx.FromGroupId, '用户 ' + command[2] + " 已成功从黑名单移除！")
				else:
					action.send_group_text_msg(ctx.FromGroupId, "黑名单移除失败！")
			else:
				action.send_group_text_msg(ctx.FromGroupId, "命令格式错误")

		elif content.split(' ', 1)[0] == 'param':
			command = content.split(' ')

			if len(command) == 4:
				# 允许的参数列表
				with open("res/json/plugins_para.json", "r") as load_file:
					json_content = json.load(load_file)

				# 命令的插件、参数允许
				if command[1] not in json_content:
					action.send_group_text_msg(ctx.FromGroupId, "插件未开启")
					return
				if command[2] not in json_content[command[1]]:
					action.send_group_text_msg(ctx.FromGroupId, "参数不存在")
					return

				key = "param." + command[2]
				para = {"$set": {key: command[3]}}
				result = plugins.update(command[1], ctx.FromGroupId, para)
				if not result["ok"] or not result["nModified"]:
					action.send_group_text_msg(ctx.FromGroupId, "参数更新失败")
					return

				action.send_group_text_msg(ctx.FromGroupId, "参数更新成功")

			else:
				action.send_group_text_msg(ctx.FromGroupId, "命令格式错误")
