# -*- coding: utf-8 -*-
import time
from iotbot import GroupMsg

import util.db.mongodb.operation as op


def receive_group_msg(ctx: GroupMsg):
    msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctx.MsgTime))
    print(f'{ctx.FromNickName}在{msg_time}的时候，发了一个类型是{ctx.MsgType}的消息，内容为：')
    print(f'{ctx.Content}')
    op.insert_group_msg(ctx)
