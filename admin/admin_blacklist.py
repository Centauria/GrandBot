# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration
from util.plugins.control import PluginControl


def admin_blacklist_group(ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_blacklist(1, ctx.Content, ctx.FromGroupId)


def admin_blacklist(flag, content, fromId):
	content = content.lstrip('.')

	if content.split(' ', 1)[0] == 'blacklist':
		command = content.split(' ')
		if len(command) == 3 and command[1] == "remove":
			plugins = PluginControl()
			if plugins.blacklist.delete(int(command[2]), fromId):
				return action_in_type(fromId, '用户 ' + command[2] + " 已成功从黑名单移除！", flag)
			else:
				return action_in_type(fromId, "黑名单移除失败！", flag)
		else:
			return action_in_type(fromId, "命令格式错误", flag)


def action_in_type(fromId, content, flag):
	if flag == 1:
		action = Action(configuration.qq)
		return action.send_group_text_msg(fromId, content)
	else:
		return content
