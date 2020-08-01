# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration
from util.plugins.control import PluginControl


# plugins管理
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:
		if ctx.MsgType == 'TextMsg':
			commands = ctx.Content.split(' ')

			if len(commands) == 2 and commands[0] == "plugins":
				plugins = PluginControl()
				action = Action(configuration.qq)

				# list命令
				if commands[1] == "list":

					results = plugins.find_all(ctx.FromGroupId)

					content = "插件列表：\n"
					for key in plugins.keywords:
						flag = 0
						for result in results:
							if key == result["plugin"]:
								flag = 1
						is_opened = '(√) ' if flag else '(×) '
						content += is_opened + key + "\n"

					action.send_group_text_msg(ctx.FromGroupId, content=content)
