# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration
from util.plugins.control import PluginControl


def admin_refresh_group(bot, ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_refresh(bot, 1, ctx.Content, ctx.FromGroupId)


def admin_refresh_friend(bot, ctx: FriendMsg):
	if ctx.FromUin in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		admin_refresh(bot, 2, ctx.Content, ctx.FromUin)


def admin_refresh(bot, flag, content, fromId):
	content = content.lstrip('.')

	if content == 'refresh':

		if flag == 1:
			bot.refresh_plugins()
			plugins = PluginControl()
			plugins.refresh()
			action = Action(configuration.qq)
			action.send_group_text_msg(fromId, '插件已刷新')
		elif flag == 2:
			bot.refresh_plugins()
			action = Action(configuration.qq)
			action.send_friend_text_msg(fromId, '插件已刷新')
		else:
			return '插件已刷新'
