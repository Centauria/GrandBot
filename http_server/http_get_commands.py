# -*- coding: utf-8 -*-
import json


# 从目录中获取BOT列表，并返回
def commandsList():
	with open("res/json/commands_list.json", 'r') as load_file:
		commands_list = json.load(load_file)
	return commands_list
