# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration

admin_command_set = ["refresh", "test", "blacklist", "param", "plugins"]


def admin_else_group(ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_else(1, ctx.Content, ctx.FromGroupId)


def admin_else_friend(ctx: FriendMsg):
	if ctx.FromUin in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_else(2, ctx.Content, ctx.FromUin)


def admin_else(flag, content, fromId):
	content = content.lstrip('.').split(" ", 1)[0]

	if content not in admin_command_set:

		if flag == 1:
			action = Action(configuration.qq)
			action.send_group_text_msg(fromId, "不要乱发指令啊喂")
		elif flag == 2:
			action = Action(configuration.qq)
			action.send_friend_text_msg(fromId, "不要乱发指令啊喂")
		else:
			return {"result": True, "content": "不要乱发指令啊喂"}
