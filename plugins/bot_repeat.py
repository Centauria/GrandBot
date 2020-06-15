# -*- coding: utf-8 -*-
import time
import json
import random
from iotbot import GroupMsg, Action

from util.config import qq

p = 0.5
delay_time = 4


def receive_group_msg(ctx: GroupMsg):
    if random.random() < p and ctx.FromUserId != qq:
        time.sleep(random.random() * delay_time)
        action = Action(qq)
        if ctx.MsgType == 'TextMsg':
            action.send_group_text_msg(ctx.FromGroupId, ctx.Content)
        elif ctx.MsgType == 'PicMsg':
            pic_msg = json.loads(ctx.Content)
            for pic_content in pic_msg['GroupPic']:
                action.send_group_pic_msg(ctx.FromGroupId, pic_content['Url'])
