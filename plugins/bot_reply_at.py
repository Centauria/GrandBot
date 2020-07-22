# -*- coding: utf-8 -*-
import json
from iotbot import GroupMsg, Action
from util import configuration
from util.network.request import get_html_text
from util.plugins.control import PluginControl


# https://www.ownthink.com/docs/bot/ ：智能回复
def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		# check
		plugin = PluginControl()
		if not plugin.check("reply_at", ctx.FromUserId, ctx.FromGroupId):
			return

		action = Action(configuration.qq)
		if ctx.MsgType == 'AtMsg':
			content = json.loads(ctx.Content)["Content"].split(" ", 1)[1]

			if content == "爬" or content == "爪巴":
				plugin.blacklist.add(ctx.FromUserId, ctx.FromGroupId, 10 * 60)
				action.send_group_text_msg(ctx.FromGroupId, content="爬什么爬，午夜凶铃啊！十分钟后再和我说话！", atUser=ctx.FromUserId)
			else:
				res_url = "https://api.ownthink.com/bot?appid=xiaosi&spoken=" + content

				res = json.loads(get_html_text(res_url))

				if res["message"] == "error":
					action.send_group_text_msg(ctx.FromGroupId, "对话请求错误！")
					return
				elif not res["data"]["type"] == 5000:
					action.send_group_text_msg(ctx.FromGroupId, "对话返回错误！")
					return
				else:
					text = res["data"]["info"]["text"]

				action.send_group_text_msg(ctx.FromGroupId, text)
