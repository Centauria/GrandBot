# -*- coding: utf-8 -*-
import os
import logging
import argparse
from iotbot import IOTBOT, Action, GroupMsg, FriendMsg

from util import configuration
from util.plugins.control import PluginControl

# python参数
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='Print loglevel=INFO')
parser.add_argument('--plugin-dir', default='plugins', help='Plugin directory')
parser.add_argument('--log-path', default=os.path.sep.join(('logs', 'log.txt')), help='Path to log file')
args = parser.parse_args()

if args.verbose:
	logging.basicConfig(level=logging.INFO)
else:
	logging.basicConfig(level=logging.ERROR)

# bot类
bot = IOTBOT(configuration.qq, use_plugins=True, plugin_dir=args.plugin_dir, log_file_path=args.log_path)
action = Action(bot)

# 插件控制类
plugins = PluginControl()


@bot.on_group_msg
def on_group_msg(ctx: GroupMsg):
	if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		content = ctx.Content.lstrip('.')
		if content == 'refresh':
			bot.refresh_plugins()
			plugins.refresh()
			print("可用插件：")
			print(plugins.keywords, '\n')
			action.send_group_text_msg(ctx.FromGroupId, '插件已刷新')
		elif content == 'test':
			action.send_group_pic_msg(ctx.FromGroupId, 'https://t.cn/A6Am7xYO')
		elif content.split(' ', 1)[0] == 'blacklist':
			command = content.split(' ')
			if len(command) == 3 and command[1] == "remove":
				if plugins.blacklist.delete(int(command[2]), ctx.FromGroupId):
					action.send_group_text_msg(ctx.FromGroupId, '用户 ' + command[2] + " 已成功从黑名单移除！")
				else:
					action.send_group_text_msg(ctx.FromGroupId, "黑名单移除失败！")
		else:
			action.send_group_text_msg(ctx.FromGroupId, '不要乱发指令啊喂')


@bot.on_friend_msg
def on_friend_msg(ctx: FriendMsg):
	if ctx.FromUin in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
		content = ctx.Content.lstrip('.')
		if content == 'refresh':
			bot.refresh_plugins()
			action.send_friend_text_msg(ctx.FromUin, '插件已刷新')
		elif content == 'test':
			action.send_friend_pic_msg(ctx.FromUin, content='', picUrl='https://t.cn/A6Am7xYO')
		else:
			action.send_friend_text_msg(ctx.FromUin, '不要乱发指令啊喂')


bot.run()
