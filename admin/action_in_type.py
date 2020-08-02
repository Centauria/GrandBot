# -*- coding: utf-8 -*-
from iotbot import Action
from util import configuration
import time


def action_in_type(fromId, content, flag, result):
	if flag == 1:
		action = Action(configuration.qq)
		res = action.send_group_text_msg(fromId, content)
		if res["Ret"] == 241:
			time.sleep(1)
			return action.send_group_text_msg(fromId, content)
		else:
			return res
	else:
		return {"result": result, "content": content}
