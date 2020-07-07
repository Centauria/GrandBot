# -*- coding: utf-8 -*-
import time
from iotbot import GroupMsg, Action
from util import configuration


# echo功能
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:
		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':

			if ctx.Content[:5] == "echo ":
				command_test = ctx.Content[5:]
				action.send_group_text_msg(ctx.FromGroupId, content=command_test)
