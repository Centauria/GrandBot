# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
import json
import time
import util.db.mongodb.operation as op
from util import configuration

# TODO: get number by jinfans.top
num = {"hentai": 4461, "drawings": 15566}


def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId == configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'PicMsg':
            pic_msg = json.loads(ctx.Content)
            content = pic_msg["Content"]
            for key in num:
                if content.find(key) != -1:
                    time.sleep(15)
                    action.revoke_msg(ctx.FromGroupId, ctx.MsgSeq, ctx.MsgRandom)
