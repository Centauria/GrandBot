# -*- coding: utf-8 -*-
import json
import logging
from pymongo.results import InsertOneResult, DeleteResult
from iotbot import GroupMsg, FriendMsg
import time

from .connection import db

logger = logging.Logger('MongoDB')


# img
def find_img_by_id(id):
	res = db.img.find_one({
		"_id": id
	})
	return res


# group_msg
def find_group_msg_by_msg_seq(msg_seq, from_group_id=None):
	if from_group_id is None:
		res = db.group_msg.find({
			"msg_seq": msg_seq
		})
	else:
		res = db.group_msg.find({
			"msg_seq": msg_seq,
			'from_group_id': from_group_id
		})
	return res.next()


def insert_group_msg(ctx: GroupMsg):
	if ctx.MsgType == 'TextMsg':
		db.group_msg.insert_one(dict(
			current_qq=ctx.CurrentQQ,
			from_nickname=ctx.FromNickName,
			from_user_id=ctx.FromUserId,
			from_group_name=ctx.FromGroupName,
			from_group_id=ctx.FromGroupId,
			at_user_id=None,
			content=ctx.Content,
			pics=None,
			tips="",
			redbag_info=ctx.RedBaginfo,
			msg_time=ctx.MsgTime,
			msg_type=ctx.MsgType,
			msg_seq=ctx.MsgSeq,
			msg_random=ctx.MsgRandom
		))
	elif ctx.MsgType == 'PicMsg':
		content = json.loads(ctx.Content)
		pics = []
		for pic in content["GroupPic"]:
			ret: InsertOneResult = db.img.insert_one(pic)
			pics.append(ret.inserted_id)
		db.group_msg.insert_one(dict(
			current_qq=ctx.CurrentQQ,
			from_nickname=ctx.FromNickName,
			from_user_id=ctx.FromUserId,
			from_group_name=ctx.FromGroupName,
			from_group_id=ctx.FromGroupId,
			at_user_id=content["UserID"] if "UserID" in content else None,
			content=content["Content"] if "Content" in content else None,
			pics=pics,
			tips=content["Tips"],
			redbag_info=ctx.RedBaginfo,
			msg_time=ctx.MsgTime,
			msg_type=ctx.MsgType,
			msg_seq=ctx.MsgSeq,
			msg_random=ctx.MsgRandom
		))
	elif ctx.MsgType == 'AtMsg':
		content = json.loads(ctx.Content)
		db.group_msg.insert_one(dict(
			current_qq=ctx.CurrentQQ,
			from_nickname=ctx.FromNickName,
			from_user_id=ctx.FromUserId,
			from_group_name=ctx.FromGroupName,
			from_group_id=ctx.FromGroupId,
			at_user_id=content["UserID"] if "UserID" in content else None,
			content=content["Content"] if "Content" in content else None,
			pics=None,
			tips=content["Tips"] if "Tips" in content else None,
			redbag_info=ctx.RedBaginfo,
			msg_time=ctx.MsgTime,
			msg_type=ctx.MsgType,
			msg_seq=ctx.MsgSeq,
			msg_random=ctx.MsgRandom
		))
	else:
		logger.error('Unspecified message type')


# friend_msg
def insert_friend_msg(ctx: FriendMsg):
	if ctx.MsgType == 'TextMsg':
		content = ctx.Content
		db.friend_msg.insert_one(dict(
			current_qq=ctx.CurrentQQ,
			from_user_id=ctx.FromUin,
			content=content["Content"] if "Content" in content else None,
			pics=None,
			tips=None,
			redbag_info=ctx.RedBaginfo,
			msg_time=int(time.time()),
			msg_type=ctx.MsgType,
			msg_seq=ctx.MsgSeq
		))
	elif ctx.MsgType == 'PicMsg':
		content = json.loads(ctx.Content)
		pics = []
		for pic in content["FriendPic"]:
			ret: InsertOneResult = db.img.insert_one(pic)
			pics.append(ret.inserted_id)
		db.friend_msg.insert_one(dict(
			current_qq=ctx.CurrentQQ,
			from_user_id=ctx.FromUin,
			content=content["Content"] if "Content" in content else None,
			pics=pics,
			tips=content["Tips"] if "Tips" in content else None,
			redbag_info=ctx.RedBaginfo,
			msg_time=int(time.time()),
			msg_type=ctx.MsgType,
			msg_seq=ctx.MsgSeq
		))
	else:
		logger.error('Unspecified message type')


# group_plugins
def insert_group_plugins(plugin, fromGroupId):
	# 是否有参数
	with open("res/json/plugins_para.json", 'r') as load_file:
		plugins_content = json.load(load_file)

	if plugins_content[plugin]:
		return db.group_plugins.insert_one(dict(
			plugin=plugin,
			from_group_id=fromGroupId,
			param=plugins_content[plugin]
		))
	else:
		return db.group_plugins.insert_one(dict(
			plugin=plugin,
			from_group_id=fromGroupId,
		))


def delete_group_plugins(plugin, fromGroupId):
	return db.group_plugins.remove({"plugin": plugin, "from_group_id": fromGroupId})


def update_group_plugins(plugin, fromGroupId, para):
	return db.group_plugins.update({"plugin": plugin, "from_group_id": fromGroupId}, para)



def count_group_plugins(plugin, fromGroupId):
	return db.group_plugins.count({"plugin": plugin, "from_group_id": fromGroupId})


def find_group_plugins(fromGroupId, plugin=""):
	if plugin == "":
		return db.group_plugins.find({"from_group_id": fromGroupId})
	else:
		return db.group_plugins.find({"plugin": plugin, "from_group_id": fromGroupId})


def find_one_group_plugins(plugin, fromGroupId):
	return db.group_plugins.find_one({"plugin": plugin, "from_group_id": fromGroupId})


# group_blacklist
def insert_group_blacklist(userId, groupId, interval, startTime=int(time.time())):
	return db.group_blacklist.insert_one(dict(
		user_id=userId,
		group_id=groupId,
		start_time=startTime,
		interval=interval
	))


def delete_group_blacklist(userId, groupId):
	return db.group_blacklist.remove({"user_id": userId, "group_id": groupId})


def count_group_blacklist(userId, groupId):
	return db.group_blacklist.count({"user_id": userId, "group_id": groupId})


def find_group_blacklist(groupId, userId=None):
	if not userId:
		return db.group_blacklist.find({"group_id": groupId})
	else:
		return db.group_blacklist.find({"user_id": userId, "group_id": groupId})


def find_one_group_blacklist(userId, groupId):
	return db.group_blacklist.find_one({"user_id": userId, "group_id": groupId})
