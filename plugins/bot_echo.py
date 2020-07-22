# -*- coding: utf-8 -*-
import time
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration
from util.plugins.control import PluginControl


# echo功能
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		# check
		plugin = PluginControl()
		if not plugin.check("echo", ctx.FromUserId, ctx.FromGroupId):
			return

		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':

			if ctx.Content[:5] == "echo ":
				command_test = ctx.Content[5:]
				action.send_group_text_msg(ctx.FromGroupId, content=command_test)


def receive_friend_msg(ctx: FriendMsg):
	action = Action(configuration.qq)
	if ctx.MsgType == 'TextMsg':

		if ctx.Content[:5] == "echo ":
			command_test = ctx.Content[5:]
			action.send_friend_text_msg(ctx.FromUin, content=command_test)
