# -*- coding: utf-8 -*-
import time
from iotbot import GroupMsg, FriendMsg

import util.db.mongodb.operation as op


def receive_group_msg(ctx: GroupMsg):
    msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctx.MsgTime))
    print(f'{ctx.FromNickName}在{msg_time}的时候，在群{ctx.FromGroupId}发了一个类型是{ctx.MsgType}的消息，内容为：')
    print(f'{ctx.Content}')
    op.insert_group_msg(ctx)


def receive_friend_msg(ctx: FriendMsg):
    print(f'{ctx.FromUin}向{ctx.ToUin}发了一个类型是{ctx.MsgType}的消息，内容为：')
    print(f'{ctx.Content}')
    op.insert_friend_msg(ctx)
