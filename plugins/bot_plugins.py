# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration
from util.plugins.control import PluginControl


# plugins管理
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:
		if ctx.MsgType == 'TextMsg':
			commands = ctx.Content.split(' ')

			if len(commands) >= 3 and commands[0] == "plugins":

				plugins = PluginControl()
				action = Action(configuration.qq)

				# open命令
				if commands[1] == "open":

					if not plugins.authority(ctx.FromUserId):
						action.send_group_text_msg(ctx.FromGroupId, content="您没有操作插件的权限")
						return

					if commands[2] in plugins.keywords:
						res = plugins.add(commands[2], ctx.FromGroupId)
						action.send_group_text_msg(ctx.FromGroupId, content=res)
					else:
						action.send_group_text_msg(ctx.FromGroupId, content=commands[2] + "不是可开启的插件")

				# close命令
				elif commands[1] == "close":

					if not plugins.authority(ctx.FromUserId):
						action.send_group_text_msg(ctx.FromGroupId, content="您没有操作插件的权限")
						return

					res = plugins.delete(commands[2], ctx.FromGroupId)
					action.send_group_text_msg(ctx.FromGroupId, content=res)

			if len(commands) == 2 and commands[0] == "plugins":
				plugins = PluginControl()
				action = Action(configuration.qq)

				# list命令
				if commands[1] == "list":
					content = "可开启的插件：\n"
					for key in plugins.keywords:
						content += key + "\n"
					content += "\n已开启的插件："
					results = plugins.find_all(ctx.FromGroupId)
					for result in results:
						content += "\n" + result["plugin"]
					action.send_group_text_msg(ctx.FromGroupId, content=content)
