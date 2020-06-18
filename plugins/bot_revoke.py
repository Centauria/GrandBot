# -*- coding: utf-8 -*-
import json
from iotbot import GroupMsg, Action
from util.db.mongodb.operation import db
from util import configuration


def receive_events(ctx: dict):
    msg_seq = ctx['CurrentPacket']['Data']['EventData']['MsgSeq']
    msg_revoke = list(db.group_msg.find({"msg_seq":msg_seq}))[0]
    print(msg_revoke)
    action = Action(configuration.qq)
    if msg_revoke["msg_type"] == 'TextMsg':
        msg = "爷发现 " + msg_revoke["from_nickname"] + " 撤回了消息：\n\n"
        action.send_group_text_msg(msg_revoke["from_group_id"], msg + msg_revoke["content"])
    if msg_revoke["msg_type"] == 'PicMsg':
        msg = "爷发现 " + msg_revoke["from_nickname"] + " 撤回了图片："
        action.send_group_text_msg(msg_revoke["from_group_id"], msg)
        pic_msg = json.loads(msg_revoke["content"])
        print(pic_msg)
        for pic_content in pic_msg['GroupPic']:
            action.send_group_pic_msg(msg_revoke["from_group_id"], fileMd5=pic_content['FileMd5'],
                                      picBase64Buf=pic_content['ForwordBuf'])



