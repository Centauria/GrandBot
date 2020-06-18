# -*- coding: utf-8 -*-
import time
from iotbot import GroupMsg, Action
from util import configuration


# 计时器功能
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            print(command)
            if command[0] == "计时" and len(command) == 2:
                try:
                    sleep_time = float(command[1])
                    time.sleep(sleep_time)
                except:
                    action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数！")