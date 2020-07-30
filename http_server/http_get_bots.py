# -*- coding: utf-8 -*-
import json
from util import configuration


# 从目录中获取BOT列表，并返回
def botsList():
	with open("res/json/bots_list.json", 'r') as load_file:
		bots_list = json.load(load_file)
	for bot in bots_list:
		if bot["version"] == "":
			bot["version"] = configuration.IOTQQVer
	return bots_list
