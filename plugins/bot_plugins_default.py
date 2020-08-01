# -*- coding: utf-8 -*-
import logging
from iotbot import Action
from util import configuration
from util.plugins.control import PluginControl

logger = logging.Logger('bot_revoke')


def receive_events(ctx: dict):
	if ctx['CurrentPacket']['Data']['EventName'] == "ON_EVENT_GROUP_JOIN" and\
			ctx['CurrentPacket']['Data']['EventData']['UserID'] == configuration.qq:
		action = Action(configuration.qq)
		plugins = PluginControl()
		msg_group_id = ctx['CurrentPacket']['Data']['EventMsg']['FromUin']

		msg = "爷来啦！\n\n默认开启插件：\n"
		for plugin_default in configuration.keywords_default:
			print(plugin_default)
			msg += plugins.add(plugin_default, msg_group_id)["content"] + '\n'
		msg.rstrip('\n')

		results = plugins.find_all(msg_group_id)

		content = "插件列表：\n"
		for key in plugins.keywords:
			flag = 0
			for result in results:
				if key == result["plugin"]:
					flag = 1
			is_opened = '(√) ' if flag else '(×) '
			content += is_opened + key + "\n"

		msg += "\n" + content

		action.send_group_text_msg(msg_group_id, msg)
