# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
import json
from util import configuration

# 分享内容
from util.network.request import get_html
from util.plugins.control import PluginControl


def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:

		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg':
			command = ctx.Content.split(' ')
			if command[0] == "点歌":

				# check
				plugin = PluginControl()
				if not plugin.check("点歌", ctx.FromUserId, ctx.FromGroupId):
					return

				if len(command) == 2:
					content = xml_get_qq(command[1])
					print(content)
					action.send_group_xml_msg(ctx.FromGroupId, content)
				if len(command) == 3:
					content = xml_get_qq(command[1], int(command[2]))
					print(content)
					action.send_group_xml_msg(ctx.FromGroupId, content)


def receive_friend_msg(ctx: FriendMsg):
	action = Action(configuration.qq)
	if ctx.MsgType == 'TextMsg':
		command = ctx.Content.split(' ')
		if command[0] == "点歌":

			if len(command) == 2:
				content = xml_get_qq(command[1])
				print(content)
				send_friend_xml_msg(action, toUser=ctx.FromUin, content=content)
			if len(command) == 3:
				content = xml_get_qq(command[1], int(command[2]))
				print(content)
				send_friend_xml_msg(action, toUser=ctx.FromUin, content=content)

		if command[0] == "json点歌":
			text = get_html("https://c.y.qq.com/soso/fcgi-bin/client_search_cp?t=0&p=1&n=1&w=真的爱你").text
			data = json.loads(text.lstrip("callback(").rstrip(')'))["data"]["song"]["list"][0]
			id = data["songid"]

			content = "{\"config\":{\"forward\":1,\"type\":\"card\",\"autosize\":1},\"prompt\":\"[应用]音乐\",\"app\":\"com.tencent.music\",\"ver\":\"0.0.0.1\",\"view\":\"Share\",\"meta\":{\"Share\":{\"musicId\":\"" + str(id) + "\"}},\"desc\":\"音乐\"}"

			print(content)
			send_friend_json_msg(action, toUser=ctx.FromUin, content=content)


def send_friend_xml_msg(action: Action, toUser: int, content='', atUser=0, timeout=5, **kwargs) -> dict:
	"""发送Xml类型信息"""
	data = {
		"toUser": toUser,
		"sendToType": 1,
		"sendMsgType": "XmlMsg",
		"content": content,
		"groupid": 0,
		"atUser": atUser
	}
	return action.baseSender('POST', 'SendMsg', data, timeout, **kwargs)


def send_friend_json_msg(action: Action, toUser: int, content='', atUser=0, timeout=5, **kwargs) -> dict:
	"""发送Xml类型信息"""
	data = {
		"toUser": toUser,
		"sendToType": 1,
		"sendMsgType": "JsonMsg",
		"content": content,
		"groupid": 0,
		"atUser": atUser
	}
	return action.baseSender('POST', 'SendMsg', data, timeout, **kwargs)


# 获得信息 info["song_name", "singer_name", "url", "image_url"]
def info_get_qq(text):
	info = []
	datas = json.loads(text.lstrip("callback(").rstrip(')'))["data"]["song"]["list"]

	if len(datas) == 0:
		return None
	data = datas[0]

	info.append(data["songname"])
	singers = ""
	for singer in data["singer"]:
		singers += singer["name"] + "/"
	info.append(singers.rstrip("/"))
	info.append(data["songmid"])
	info.append(data["albumname"])

	return info


def info_image_get_qq(text):
	datas = json.loads(text.lstrip("callback(").rstrip(')'))["data"]["album"]["list"]

	if len(datas) == 0:
		return None

	return datas[0]["albumPic"]


# TODO: get these long xml into `res/xml` folder
def xml_get_qq(key, num=1):
	info = info_get_qq(
		get_html("https://c.y.qq.com/soso/fcgi-bin/client_search_cp?t=0&p=" + f"""{num}""" + "&n=1&w=" + key).text)
	if not info:
		return None

	image = info_image_get_qq(
		get_html("https://c.y.qq.com/soso/fcgi-bin/client_search_cp?t=8&p=1&n=1&w=" + info[3]).text)
	if not image:
		info.append("")
	info.append(image)

	xml = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID=\"123\" "
	xml += " url=\"https://i.y.qq.com/v8/playsong.html?platform=11&amp;songmid=" + f"""{info[2]}\" """
	xml += " serviceID=\"1\" action=\"web\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[分享]" + f"""{info[0]}""" + "\" flag=\"0\"><item layout=\"2\"> "
	xml += " <picture cover=\"" + f"""{info[4]}""" + "\"/> "
	xml += " <title>" + f"""{info[0]}""" + "</title><summary>" + f"""{info[1]}""" + "</summary> "
	xml += " </item><source url=\"\" icon=\"\" name=\"QQ音乐\" appid=\"100497308\" action=\"\" actionData=\"\" a_actionData=\"tencent100497308://\" i_actionData=\"\"/></msg>"
	return xml
