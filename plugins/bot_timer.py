# -*- coding: utf-8 -*-
import time
from iotbot import GroupMsg, Action
from util import configuration
from util.plugins.control import PluginControl

time_words = {'minutes': 60, 'hours': 3600, 'days': 24 * 3600, 's': 1, '秒': 1, 'm': 60, 'min': 60, 'minute': 60,
			  '分': 60, '分钟': 60, 'h': 3600, 'hour': 3600, '小时': 3600, 'd': 24 * 3600, 'day': 24 * 3600, '天': 24 * 3600}
alarm_words = {"%Y/%m/%d %H:%M:%S": 0, "%Y-%m-%d %H:%M:%S": 0, "%Y%m%d%H%M%S": 0, "%H:%M:%S": "%Y/%m/%d %H:%M:%S"}


def time_shift(time_str):
	try:
		for key in time_words:
			length = len(key)
			if time_str[-length:] == key:
				return time_words[key] * float(time_str.rstrip(key))
	except Exception as e:
		return False


def alarm_shift(time_str):
	for key in alarm_words:
		try:
			if alarm_words[key] == 0:
				return time.strptime(time_str, key)
			else:
				date = time.strftime("%Y/%m/%d ", time.localtime())
				return time.strptime(date + time_str, alarm_words[key])
		except Exception as e:
			continue
	return False


# 计时器功能
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':

			if ctx.Content[:3] == "计时 ":

				# check
				plugin = PluginControl()
				if not plugin.check("计时", ctx.FromGroupId):
					return

				command_time = ctx.Content.lstrip("计时 ")
				if time_shift(command_time):
					sleep_time = time_shift(command_time)
					if sleep_time > 4294967:
						action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数：\n设置时间过长！")
					elif sleep_time < 0:
						action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数：\n设置时间为负！")
					else:
						action.send_group_text_msg(ctx.FromGroupId, "爷开始计时啦！")
						time.sleep(sleep_time)
						msg = " 计时 " + command_time + " 结束！"
						action.send_group_text_msg(ctx.FromGroupId, atUser=ctx.FromUserId, content=msg)
				else:
					action.send_group_text_msg(ctx.FromGroupId, "非法时间格式！")

			if ctx.Content[:3] == "闹钟 ":

				# check
				plugin = PluginControl()
				if not plugin.check("闹钟", ctx.FromGroupId):
					return

				command = ctx.Content.lstrip("闹钟 ").split(' ', 1)
				time_array = alarm_shift(command[1])
				if time_array:
					time_stamp = int(time.mktime(time_array))
					sleep_time = time_stamp - int(time.time())
					print(sleep_time)
					if sleep_time <= 0:
						action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数：\n设定时间已过！")
					else:
						action.send_group_text_msg(ctx.FromGroupId, "爷设好闹钟啦！")
						time.sleep(sleep_time)
						msg = " 闹钟 " + f"""{command[0]}""" + " 到时间啦！"
						action.send_group_text_msg(ctx.FromGroupId, atUser=ctx.FromUserId, content=msg)
				else:
					action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数：\n非法时间格式！")


