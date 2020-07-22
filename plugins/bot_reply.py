# -*- coding: utf-8 -*-
import time
import json
import random
from iotbot import GroupMsg, Action

from util import configuration

from util.db.mongodb.operation import db
from util.plugins.control import PluginControl


# 收到消息以p的概率回复
# 回复时以q的概率复读

# mongo/bot/group_msg_reply {type:消息处理类型; key:检索关键词; reply:回复关键词; [pos:(type=1时)key出现的位置]}
# type=0, 当msg=key时，回复reply
# type=1, 当key出现在msg的第pos位置时，回复reply
#    pos>=0：从0开始计数，字符的下标
#    pos=-1：末尾匹配
#    pos=-2：任意位置
# type=2, 当key出现在msg的第pos位置时，用reply替换并复读


def receive_group_msg(ctx: GroupMsg):
	# check
	plugin = PluginControl()
	if not plugin.check("reply", ctx.FromUserId, ctx.FromGroupId):
		return

	# param
	param = plugin.find_one("reply", ctx.FromGroupId)["param"]
	p = float(param["p"])
	q = float(param["q"])
	delay_time = float(param["delay_time"])

	if random.random() < p and ctx.FromUserId != configuration.qq:
		time.sleep(random.random() * delay_time)
		action = Action(configuration.qq)
		if ctx.MsgType == 'TextMsg' and not plugin.is_command(ctx.Content.split(' ', 1)[0], ctx.FromGroupId):
			action.send_group_text_msg(ctx.FromGroupId, replace_text_msg(ctx.Content, q))
		elif ctx.MsgType == 'PicMsg':
			pic_msg = json.loads(ctx.Content)
			for pic_content in pic_msg['GroupPic']:
				action.send_group_pic_msg(ctx.FromGroupId, fileMd5=pic_content['FileMd5'],
										  picBase64Buf=pic_content['ForwordBuf'])


# 复读替换关键词
def replace_text_msg(msg, q):
	r = random.random()
	reply_set = []
	s = msg
	for x in db.group_msg_reply.find():

		type = x["type"]
		key = x["key"]
		reply = x["reply"]
		if type != 0:
			pos = int(x["pos"])

		if msg == key and type == 0:  # type = 0
			return reply
		elif r > q and type == 1 and judge_pos(msg, key, pos):  # type = 1
			reply_set.append(reply)
		elif r <= q and type == 2:  # type = 2
			s = replace_pos(s, key, reply, pos)

	if r <= q:
		return s
	elif not reply_set:
		return s
	else:
		n = random.randint(0, len(reply_set) - 1)
		return reply_set[n]


# 判断key是否以pos要求的形式存在于msg中
def judge_pos(msg, key, pos):
	if pos == -2:
		if msg.find(key) != -1:
			return True
	elif pos == -1:
		for i in range(len(key)):
			if msg[-i - 1] != key[-i - 1]:
				return False
		return True
	else:
		# 检验是否相同
		for i in range(len(key)):
			if msg[pos + i] != key[i]:
				return False
		return True


# 以pos要求的形式替换msg中的key
def replace_pos(msg, key, reply, pos):
	if pos == -2:
		return msg.replace(key, reply)
	elif pos == -1:
		# 检验是否相同
		for i in range(len(key)):
			if msg[-i - 1] != key[-i - 1]:
				return msg
		# 替换
		s = msg[0:len(msg) - len(key)]
		s = s + reply
		return s
	else:
		# 检验是否相同
		for i in range(len(key)):
			if msg[pos + i] != key[i]:
				return msg
		# 替换
		s = msg[0:pos]
		s = s + reply
		s = s + msg[pos + len(key):]
		return s
