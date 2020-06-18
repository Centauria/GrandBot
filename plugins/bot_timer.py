# -*- coding: utf-8 -*-
import time
from iotbot import GroupMsg, Action
from util import configuration


# 计时器功能
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':

            if ctx.Content[:3] == "计时 ":
                try:
                    command_time = ctx.Content.lstrip("计时")
                    sleep_time = float(command_time)
                    action.send_group_text_msg(ctx.FromGroupId, "爷开始计时啦！")
                    time.sleep(sleep_time)
                    action.send_group_text_msg(ctx.FromGroupId, atUser=ctx.FromUserId,
                                               content="计时" + f"""{command_time}""" + "s 结束！")
                except:
                    action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数！")

            if ctx.Content[:3] == "闹钟 ":
                try:
                    command = ctx.Content.lstrip("闹钟 ").split(' ', 1)
                    timeArray = time.strptime(command[1], "%Y/%m/%d %H:%M:%S")
                    timeStamp = int(time.mktime(timeArray))
                    action.send_group_text_msg(ctx.FromGroupId, "爷设好闹钟啦！")
                    sleep_time = timeStamp - int(time.time())
                    if sleep_time <= 0:
                        action.send_group_text_msg(ctx.FromGroupId, "设定时间有误！")
                    else:
                        time.sleep(sleep_time)
                        msg = " 闹钟 " + f"""{command[0]}""" + " 到时间啦！"
                        action.send_group_text_msg(ctx.FromGroupId, atUser=ctx.FromUserId, content=msg)
                except:
                    action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数！")
