# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration
from util.plugins.control import PluginControl
import subprocess
import os


# echo功能
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		# check
		plugin = PluginControl()
		if not plugin.check("python", ctx.FromUserId, ctx.FromGroupId):
			return

		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':

			command = ctx.Content.split(' ')
			if command[0] == "runpython" and len(command) == 2:

				if not judge_name(command[1]):
					action.send_group_text_msg(ctx.FromGroupId, content="文件名非法")
					return

				res = runpy(command[1])
				action.send_group_text_msg(ctx.FromGroupId, content=res)

			# 判断用\r还是\n
			char_r = ctx.Content.find('\r')
			char_n = ctx.Content.find('\n')
			if (char_r < char_n and char_r != -1) or char_n == -1:
				char = '\r'
			else:
				char = '\n'

			all_content = ctx.Content.split(char, 1)

			if len(all_content) == 2:
				command = all_content[0].split(' ')
				pycontent = all_content[1]

			if len(command) == 2 and command[0] == "newpython" and command[1][-3:] == ".py":

				if not judge_name(command[1]):
					action.send_group_text_msg(ctx.FromGroupId, content="文件名非法")
					return

				if not judge_py(pycontent):
					action.send_group_text_msg(ctx.FromGroupId, " 文件包含不允许的字符串")
					return

				res = newpy(command[1], pycontent)

				if res:
					action.send_group_text_msg(ctx.FromGroupId, content=command[1] + " 创建成功")
				else:
					action.send_group_text_msg(ctx.FromGroupId, content="文件创建失败")


def receive_friend_msg(ctx: FriendMsg):
	action = Action(configuration.qq)
	if ctx.MsgType == 'TextMsg':

		command = ctx.Content.split(' ')
		if command[0] == "runpython" and len(command) == 2:

			if not judge_name(command[1]):
				action.send_friend_text_msg(ctx.FromUin, content="文件名非法")
				return

			res = runpy(command[1])
			action.send_friend_text_msg(ctx.FromUin, content=res)

		# 判断用\r还是\n
		char_r = ctx.Content.find('\r')
		char_n = ctx.Content.find('\n')
		if (char_r < char_n and char_r != -1) or char_n == -1:
			char = '\r'
		else:
			char = '\n'

		print(char_r, char_n, char_r < char_n or char_n == -1, char)

		all_content = ctx.Content.split(char, 1)

		if len(all_content) == 2:
			command = all_content[0].split(' ')
			pycontent = all_content[1]

		if len(command) == 2 and command[0] == "newpython" and command[1][-3:] == ".py":

			if not judge_name(command[1]):
				action.send_friend_text_msg(ctx.FromUin, content="文件名非法")
				return

			if not judge_py(pycontent):
				action.send_friend_text_msg(ctx.FromUin, content="文件包含不允许的字符串")
				return

			res = newpy(command[1], pycontent)
			if res:
				action.send_friend_text_msg(ctx.FromUin, content=command[1] + " 创建成功")
			else:
				action.send_friend_text_msg(ctx.FromUin, content="文件创建失败")


# 创建python文件
def newpy(pyname: str, content: str):
	path = "res/python/" + pyname
	if os.path.isfile(path):
		return False
	else:
		with open(path, "w") as py_file:
			py_file.write(content)
			py_file.close()
		return True


def judge_name(pyname: str):
	if pyname.find("..") != -1 or pyname.find("\\") != -1 or pyname.find("/") != -1:
		return False
	return True


# 检验创建的python文件中有无非法操作
def judge_py(content: str):
	bypass = ["system(", "Popen(", "open(", "import os", "from os", "import commands", "from commands"
		, "import subprocess", "from subprocess", "import importlib", "from importlib", "eval", "exec"]
	for key in bypass:
		if content.find(key) != -1:
			return False
	return True


# 运行python文件，返回结果
def runpy(pyname: str):
	path = "res/python/" + pyname
	child = subprocess.Popen(["python", path], stdout=subprocess.PIPE, encoding="utf8")
	res = str(child.stdout.read())
	child.kill()

	return res
