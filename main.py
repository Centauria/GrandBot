# -*- coding: utf-8 -*-
import os
import logging
import argparse
import _thread
from functools import partial
from iotbot import IOTBOT, Action

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

# admin命令接受

from admin.admin_else import admin_else_group, admin_else_friend

bot.add_group_msg_receiver(admin_else_group)
bot.add_friend_msg_receiver(admin_else_friend)

from admin.admin_refresh import admin_refresh_group, admin_refresh_friend

bot.add_group_msg_receiver(partial(admin_refresh_group, bot))
bot.add_friend_msg_receiver(partial(admin_refresh_friend, bot))

from admin.admin_test import admin_test_group, admin_test_friend

bot.add_group_msg_receiver(admin_test_group)
bot.add_friend_msg_receiver(admin_test_friend)

from admin.admin_blacklist import admin_blacklist_group

bot.add_group_msg_receiver(admin_blacklist_group)

from admin.admin_param import admin_param_group

bot.add_group_msg_receiver(admin_param_group)

# HTTP Server for admin
from http_server.http_server import *

_thread.start_new_thread(app.run, ("127.0.0.1", 9001,))


# 需要引用bot的命令
@app.route('/refresh', methods=['GET', 'POST'])
def http_refresh():
	content = ".refresh"
	fromId = 0
	return http_refresh_raw(bot, content, fromId)


bot.run()
