# -*- coding: utf-8 -*-
import json
from iotbot import GroupMsg, Action
import util.db.mongodb.operation as op
from util import configuration


def receive_events(ctx: dict):
    msg_seq = ctx['CurrentPacket']['Data']['EventData']['MsgSeq']
    print(f'{msg_seq}')
    msg_revoke = op.find_group_msg_by_msgseq(msg_seq)
    action = Action(configuration.qq)
    if msg_revoke["msg_type"] == 'TextMsg':
        msg = "爷发现 " + msg_revoke["from_nickname"] + " 撤回了消息！\n"
        print(msg_revoke["content"])
        action.send_group_text_msg(msg_revoke["from_group_id"], msg)

