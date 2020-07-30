# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration


def admin_test_group(ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_test(1, ctx.Content, ctx.FromGroupId)


def admin_test_friend(ctx: FriendMsg):
	if ctx.FromUin in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_test(2, ctx.Content, ctx.FromUin)


def admin_test(flag, content, fromId):
	content = content.lstrip('.')

	if content == 'test':

		if flag == 1:
			action = Action(configuration.qq)
			action.send_group_pic_msg(fromId, 'https://t.cn/A6Am7xYO')
		elif flag == 2:
			action = Action(configuration.qq)
			action.send_friend_pic_msg(fromId, 'https://t.cn/A6Am7xYO')
		else:
			return {"result": True, "content": 'https://t.cn/A6Am7xYO'}
