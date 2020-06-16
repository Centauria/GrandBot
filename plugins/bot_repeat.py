# -*- coding: utf-8 -*-
import time
import json
import random
from iotbot import GroupMsg, Action

from util import configuration

p = 0.5
delay_time = 4


def receive_group_msg(ctx: GroupMsg):
    if random.random() < p and ctx.FromUserId != configuration.qq:
        time.sleep(random.random() * delay_time)
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            action.send_group_text_msg(ctx.FromGroupId, replace_wo_ye(ctx.Content))
        elif ctx.MsgType == 'PicMsg':
            pic_msg = json.loads(ctx.Content)
            for pic_content in pic_msg['GroupPic']:
                action.send_group_pic_msg(ctx.FromGroupId, fileMd5=pic_content['FileMd5'],
                                          picBase64Buf=pic_content['ForwordBuf'])


def replace_wo_ye(text):
    s = list(text)
    for i in range(len(s)):
        if s[i] == '我':
            s[i] = '爷'
    return "".join(s)
