# -*- coding: utf-8 -*-
import logging
from iotbot import Action
from util.db.mongodb.operation import db, find_group_msg_by_msg_seq, find_img_by_id
from util import configuration
from util.plugins.control import PluginControl

logger = logging.Logger('bot_revoke')


def receive_events(ctx: dict):

    # check
    plugin = PluginControl()
    if not plugin.check("防撤回", ctx['CurrentPacket']['Data']['EventData']['GroupID']):
        return

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
            msg = "爷发现 " + msg_revoke["from_nickname"] + " 撤回了图片：\n\n"
            msg_content = msg_revoke["content"] if msg_revoke["content"] is not None else ""
            action.send_group_text_msg(msg_revoke["from_group_id"], msg + msg_content)
            pics = msg_revoke["pics"]
            for pic_id in pics:
                pic_content = find_img_by_id(pic_id)
                action.send_group_pic_msg(
                    msg_revoke["from_group_id"],
                    fileMd5=pic_content['FileMd5'],
                    picBase64Buf=pic_content['ForwordBuf']
                )
