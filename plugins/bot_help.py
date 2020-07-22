# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
import json
from util import configuration

# help
from util.plugins.control import PluginControl


def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':
			command = ctx.Content.split(' ')
			if command[0] == "help":

				# check
				plugin = PluginControl()
				if not plugin.check("help", ctx.FromUserId, ctx.FromGroupId):
					return

				with open("res/json/help_group.json", 'r') as load_file:
					help_content = json.load(load_file)

				if len(command) == 1:

					content = "帮助：\n"
					for key, value in help_content.items():
						if key in plugin.keywords:
							content += '\n' + value + '\n'

					action.send_group_text_msg(ctx.FromGroupId, content)

				elif len(command) == 2 and command[1] == "admin":

					content = "管理员帮助：\n"

					with open("res/json/help_admin.json", 'r') as load_file:
						help_content = json.load(load_file)

					for key, value in help_content.items():
						content += '\n' + value + '\n'

					action.send_group_text_msg(ctx.FromGroupId, content)

				elif len(command) == 2:

					content = "帮助："
					for key, value in help_content.items():
						if command[1] == key and key in plugin.keywords:
							content += value

					if not content == "帮助：":
						action.send_group_text_msg(ctx.FromGroupId, content)


def receive_friend_msg(ctx: FriendMsg):
	action = Action(configuration.qq)
	if ctx.MsgType == 'TextMsg':
		command = ctx.Content.split(' ')
		if command[0] == "help":

			plugin = PluginControl()

			with open("res/json/help_friend.json", 'r') as load_file:
				help_content = json.load(load_file)

			if len(command) == 1:

				content = "帮助：\n"
				for key, value in help_content.items():
					if key in plugin.keywords:
						content += '\n' + value + '\n'

				action.send_friend_text_msg(ctx.FromUin, content)

			elif len(command) == 2:

				content = "帮助："
				for key, value in help_content.items():
					if command[1] == key and key in plugin.keywords:
						content += value

				if not content == "帮助：":
					action.send_friend_text_msg(ctx.FromUin, content)
