# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
import util.db.mongodb.operation as op
from util import configuration

num = {"hentai": 4461, "drawings": 15566}


def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'PicMsg':
            content = ctx.Content["Content"]
            for key in num:
                if content.find(key) != -1:
                    msg_revoke = list(op.find_group_msg_by_pic_content(content))
                    print(msg_revoke)
