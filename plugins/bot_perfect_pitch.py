# -*- coding: utf-8 -*-
import time
import random
import numpy as np

from iotbot import GroupMsg, FriendMsg, Action
from util import configuration
from util.plugins.control import PluginControl

key_sets = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def random_pitch(num: int):
	key = int(num % 12)
	octive = int(np.floor((num - 3) / 12)) + 1

	name = key_sets[key] + str(octive)

	return name


def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':
			command = ctx.Content
			if command == "绝对音感测试":

				# check
				plugin = PluginControl()
				if not plugin.check("绝对音感测试", ctx.FromUserId, ctx.FromGroupId):
					return

				param = plugin.find_one("绝对音感测试", ctx.FromGroupId)["param"]

				sleep_time = int(param["time"])
				low = int(param["low"])
				high = int(param["high"])

				num = random.randint(low, high)
				key = random_pitch(num)

				url = "http://jinfans.top/others/perfect_pitch/" + str(num) + ".mp3"
				print(url)

				action.send_group_voice_msg(ctx.FromGroupId, url)

				action.send_group_text_msg(ctx.FromGroupId, "绝对音感测试开始！" + str(sleep_time) + "s后公布答案")

				time.sleep(sleep_time)
				action.send_group_text_msg(ctx.FromGroupId, "正确答案是：" + key)
