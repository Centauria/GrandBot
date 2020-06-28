# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
import time
from util import configuration


def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId == configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'PicMsg':
            labels = ["drawings", "hentai", "neutral", "porn", "sexy"]
            for key in labels:
                if ctx.Content.find(key) != -1:
                    time.sleep(15)
                    action.revoke_msg(ctx.FromGroupId, ctx.MsgSeq, ctx.MsgRandom)
