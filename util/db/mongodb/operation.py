# -*- coding: utf-8 -*-
import json
import logging
from pymongo.results import InsertOneResult
from iotbot import GroupMsg, FriendMsg

from .connection import db

logger = logging.Logger('MongoDB')


def find_group_msg_by_msg_seq(msg_seq, from_group_id=None):
    if from_group_id is None:
        res = db.group_msg.find({
            "msg_seq": msg_seq
        })
    else:
        res = db.group_msg.find({
            "msg_seq": msg_seq,
            'from_group_id': from_group_id
        })
    return res.next()


def find_group_msg_by_pic_content(msg_content):
    return db.group_msg.find({"msg_type": "PicMsg", "content.Content": msg_content}).sort({"msg_time": -1}).limit(1)


def insert_group_msg(ctx: GroupMsg):
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


def insert_friend_msg(ctx: FriendMsg):
    if ctx.MsgType == 'TextMsg':
        content = ctx.Content
        db.friend_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_user_id=ctx.FromUin,
            content=content,
            redbag_info=ctx.RedBaginfo,
            msg_time='???',
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
        ))
    elif ctx.MsgType == 'PicMsg':
        content = json.loads(ctx.Content)
        ret: InsertOneResult = db.img.insert_one(content)
        db.friend_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_user_id=ctx.FromUin,
            content=content,
            redbag_info=ctx.RedBaginfo,
            msg_time='???',
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
        ))
    elif ctx.MsgType == 'AtMsg':
        db.friend_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_user_id=ctx.FromUin,
            content=ctx.Content,
            redbag_info=ctx.RedBaginfo,
            msg_time='???',
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
        ))
    else:
        logger.error('Unspecified message type')
