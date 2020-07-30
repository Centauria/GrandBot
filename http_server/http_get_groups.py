# -*- coding: utf-8 -*-
from iotbot import Action
from util import configuration
from util.plugins.control import PluginControl


def groupsList(content):
	command = content.split(" ", 1)
	if len(command) == 2 and command[0] == '.groups' and command[1] == str(configuration.qq):
		action = Action(configuration.qq)
		lists = action.get_group_list()["TroopList"]
		id = 1
		for group in lists:
			group["pluginsNum"] = pluginsNum(group["GroupId"])
			group["id"] = id
			id += 1
		return lists
	else:
		return [{
			"id": 0,
			"GroupId": 0,
			"GroupMemberCount": 0,
			"GroupName": "NULL",
			"GroupNotice": "IP Wrong",
			"GroupOwner": 0,
			"pluginsNum": 0
		}]


def pluginsNum(groupId):
	return len(PluginControl().find_all(groupId))
