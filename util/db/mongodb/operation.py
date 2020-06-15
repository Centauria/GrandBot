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
            content=ret.inserted_id,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
        ))
    elif ctx.MsgType == 'AtMsg':
        content = json.loads(ctx.Content)
        db.group_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            content=content['Content'],
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            at_id=content['UserID']
        ))
    else:
        logger.error('Unspecified message type')
