# -*- coding: utf-8 -*-
import json
import logging
from pymongo.results import InsertOneResult
from iotbot import GroupMsg, FriendMsg
import time

from .connection import db

logger = logging.Logger('MongoDB')


def find_img_by_id(id):
    res = db.img.find_one({
        "_id": id
    })
    return res


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


def insert_group_msg(ctx: GroupMsg):
    if ctx.MsgType == 'TextMsg':
        db.group_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            at_user_id=None,
            content=ctx.Content,
            pics=None,
            tips="",
            redbag_info=ctx.RedBaginfo,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            msg_random=ctx.MsgRandom
        ))
    elif ctx.MsgType == 'PicMsg':
        content = json.loads(ctx.Content)
        pics = []
        for pic in content["GroupPic"]:
            ret: InsertOneResult = db.img.insert_one(pic)
            pics.append(ret.inserted_id)
        db.group_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            at_user_id=content["UserID"] if "UserID" in content else None,
            content=content["Content"] if "Content" in content else None,
            pics=pics,
            tips=content["Tips"],
            redbag_info=ctx.RedBaginfo,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            msg_random=ctx.MsgRandom
        ))
    elif ctx.MsgType == 'AtMsg':
        content = json.loads(ctx.Content)
        db.group_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            at_user_id=content["UserID"] if "UserID" in content else None,
            content=content["Content"] if "Content" in content else None,
            pics=None,
            tips=content["Tips"] if "Tips" in content else None,
            redbag_info=ctx.RedBaginfo,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            msg_random=ctx.MsgRandom
        ))
    else:
        logger.error('Unspecified message type')


def insert_friend_msg(ctx: FriendMsg):
    if ctx.MsgType == 'TextMsg':
        content = ctx.Content
        db.friend_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_user_id=ctx.FromUin,
            content=content["Content"] if "Content" in content else None,
            pics=None,
            tips=None,
            redbag_info=ctx.RedBaginfo,
            msg_time=int(time.time()),
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq
        ))
    elif ctx.MsgType == 'PicMsg':
        content = json.loads(ctx.Content)
        pics = []
        for pic in content["FriendPic"]:
            ret: InsertOneResult = db.img.insert_one(pic)
            pics.append(ret.inserted_id)
        db.friend_msg.insert_one(dict(
            current_qq=ctx.CurrentQQ,
            from_user_id=ctx.FromUin,
            content=content["Content"] if "Content" in content else None,
            pics=pics,
            tips=content["Tips"] if "Tips" in content else None,
            redbag_info=ctx.RedBaginfo,
            msg_time=int(time.time()),
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq
        ))
    else:
        logger.error('Unspecified message type')
