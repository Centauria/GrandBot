# -*- coding: utf-8 -*-
import json
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration
from util.network.request import get_html_text
from util.plugins.control import PluginControl


# 输入文字，以语音形式发送
# https://www.duiopen.com/docs/ct_cloud_TTS_web API：文字转语音
# https://www.ownthink.com/docs/bot/ ：智能回复
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':
			command = ctx.Content.split(' ')
			if command[0] == "说话" and len(command) >= 2:

				# check
				plugin = PluginControl()
				if not plugin.check("说话", ctx.FromUserId, ctx.FromGroupId):
					return

				text = command[1]
				voiceId = "geyou"
				speed = "1.5"
				volume = "100"
				audioType = "wav"
				for i in range(len(command) - 2):
					if command[i + 2][:8] == 'voiceId=':
						voiceId = command[i + 2].lstrip('voice=Id')
					elif command[i + 2][:6] == 'speed=':
						speed = command[i + 2].lstrip('speed=')
					elif command[i + 2][:7] == 'volume=':
						volume = command[i + 2].lstrip('volume=')
					elif command[i + 2][:10] == 'audioType=':
						audioType = command[i + 2].lstrip('audioType=')

				url = "https://dds.dui.ai/runtime/v1/synthesize?voiceId=" + voiceId + "&speed=" + speed + \
					  "&volume=" + volume + "&audioType=" + audioType + "&text=" + text

				action.send_group_voice_msg(ctx.FromGroupId, url)

			elif command[0] == "对话" and len(command) >= 2:

				# check
				plugin = PluginControl()
				if not plugin.check("对话", ctx.FromUserId, ctx.FromGroupId):
					return

				ask = command[1]
				voiceId = "geyou"
				speed = "1.5"
				volume = "100"
				audioType = "wav"
				for i in range(len(command) - 2):
					if command[i + 2][:8] == 'voiceId=':
						voiceId = command[i + 2].lstrip('voice=Id')
					elif command[i + 2][:6] == 'speed=':
						speed = command[i + 2].lstrip('speed=')
					elif command[i + 2][:7] == 'volume=':
						volume = command[i + 2].lstrip('volume=')
					elif command[i + 2][:10] == 'audioType=':
						audioType = command[i + 2].lstrip('audioType=')

				res_url = "https://api.ownthink.com/bot?appid=xiaosi&spoken=" + ask

				res = json.loads(get_html_text(res_url))

				print(res)
				if res["message"] == "error":
					action.send_group_text_msg(ctx.FromGroupId, "对话请求错误！")
					return
				elif not res["data"]["type"] == 5000:
					action.send_group_text_msg(ctx.FromGroupId, "对话返回错误！")
					return
				else:
					text = res["data"]["info"]["text"]

				url = "https://dds.dui.ai/runtime/v1/synthesize?voiceId=" + voiceId + "&speed=" + speed + \
					  "&volume=" + volume + "&audioType=" + audioType + "&text=" + text

				action.send_group_voice_msg(ctx.FromGroupId, url)


def receive_friend_msg(ctx: FriendMsg):
	action = Action(configuration.qq)
	if ctx.MsgType == 'TextMsg':
		command = ctx.Content.split(' ')
		if command[0] == "说话" and len(command) >= 2:

			text = command[1]
			voiceId = "geyou"
			speed = "1.5"
			volume = "100"
			audioType = "wav"
			for i in range(len(command) - 2):
				if command[i + 2][:8] == 'voiceId=':
					voiceId = command[i + 2].lstrip('voice=Id')
				elif command[i + 2][:6] == 'speed=':
					speed = command[i + 2].lstrip('speed=')
				elif command[i + 2][:7] == 'volume=':
					volume = command[i + 2].lstrip('volume=')
				elif command[i + 2][:10] == 'audioType=':
					audioType = command[i + 2].lstrip('audioType=')

			url = "https://dds.dui.ai/runtime/v1/synthesize?voiceId=" + voiceId + "&speed=" + speed + \
				  "&volume=" + volume + "&audioType=" + audioType + "&text=" + text

			action.send_friend_voice_msg(ctx.FromUin, url)

		elif command[0] == "对话" and len(command) >= 2:

			ask = command[1]
			voiceId = "geyou"
			speed = "1.5"
			volume = "100"
			audioType = "wav"
			for i in range(len(command) - 2):
				if command[i + 2][:8] == 'voiceId=':
					voiceId = command[i + 2].lstrip('voice=Id')
				elif command[i + 2][:6] == 'speed=':
					speed = command[i + 2].lstrip('speed=')
				elif command[i + 2][:7] == 'volume=':
					volume = command[i + 2].lstrip('volume=')
				elif command[i + 2][:10] == 'audioType=':
					audioType = command[i + 2].lstrip('audioType=')

			res_url = "https://api.ownthink.com/bot?appid=xiaosi&spoken=" + ask

			res = json.loads(get_html_text(res_url))

			print(res)
			if res["message"] == "error":
				action.send_friend_text_msg(ctx.FromUin, "对话请求错误！")
				return
			elif not res["data"]["type"] == 5000:
				action.send_friend_text_msg(ctx.FromUin, "对话返回错误！")
				return
			else:
				text = res["data"]["info"]["text"]

			url = "https://dds.dui.ai/runtime/v1/synthesize?voiceId=" + voiceId + "&speed=" + speed + \
				  "&volume=" + volume + "&audioType=" + audioType + "&text=" + text

			action.send_friend_voice_msg(ctx.FromUin, url)
