# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
from util.db.mongodb.operation import db
from util import configuration

num = {"hentai": 4461, "drawings": 15566}

def receive_group_msg(ctx: GroupMsg):
	if ctx.FromUserId != configuration.qq:
		action = Action(configuration.qq)
		if ctx.MsgType == 'PicMsg':
			content = ctx.Content["Content"]
			for key in num:
				if content.find(key) != -1:
        			msg_revoke = list(db.group_msg.find({"msg_seq": msg_seq, 'from_group_id': msg_group_id}))[0]
