# -*- coding: utf-8 -*-
import logging
from iotbot import Action
from util.db.mongodb.operation import db, find_group_msg_by_msg_seq
from util import configuration

logger = logging.Logger('bot_revoke')


def receive_events(ctx: dict):
    if ctx['CurrentPacket']['Data']['EventData']['UserID'] != configuration.qq and \
            ctx['CurrentPacket']['Data']['EventName'] == 'ON_EVENT_GROUP_REVOKE':
        action = Action(configuration.qq)
        msg_set = ctx['CurrentPacket']['Data']['EventData']
        msg_seq = msg_set['MsgSeq']
        msg_group_id = msg_set['GroupID']
        msg_revoke = find_group_msg_by_msg_seq(msg_seq, msg_group_id)
        if msg_revoke is None:
            logger.error('db.find returns null result')
            return
        if msg_revoke["msg_type"] == 'TextMsg':
            msg = "爷发现 " + msg_revoke["from_nickname"] + " 撤回了消息：\n\n"
            action.send_group_text_msg(msg_revoke["from_group_id"], msg + msg_revoke["content"])
        if msg_revoke["msg_type"] == 'PicMsg':
            msg = "爷发现 " + msg_revoke["from_nickname"] + " 撤回了图片："
            action.send_group_text_msg(msg_revoke["from_group_id"], msg)
            pic_msg = msg_revoke["content"]
            for pic_content in pic_msg['GroupPic']:
                action.send_group_pic_msg(
                    msg_revoke["from_group_id"],
                    fileMd5=pic_content['FileMd5'],
                    picBase64Buf=pic_content['ForwordBuf']
                )
