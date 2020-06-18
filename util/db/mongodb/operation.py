# -*- coding: utf-8 -*-
import json
import logging
from pymongo.results import InsertOneResult

from .connection import db

logger = logging.Logger('MongoDB')


def insert_group_msg(ctx):
    if ctx.MsgType == 'TextMsg':
        content = ctx.Content
        db.group_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            content=content,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
        ))
    elif ctx.MsgType == 'PicMsg':
        content = json.loads(ctx.Content)
        ret: InsertOneResult = db.img.insert_one(content)
        db.group_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            content=content,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
        ))
    elif ctx.MsgType == 'AtMsg':
        db.group_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            content=ctx.Content,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
        ))
    else:
        logger.error('Unspecified message type')


def find_group_msg_by_msgseq(msg_seq):
    return db.group_nsg.find({"msg_seq":msg_seq}).sort({"uploadTime": -1})