# -*- coding: utf-8 -*-
import random
from iotbot import FriendMsg, Action
from util import configuration


# 输入 “百度 关键字”，回显百科内容
def receive_friend_msg(ctx: FriendMsg):
    action = Action(configuration.qq)
    if ctx.MsgType == 'TextMsg':
        command = ctx.Content.split(' ')
        if command[0] == "setu":
            execute = "hentai"
            no = random.randint(1, 4611)
            name = execute + "{:0>5d}".format(no) + '.png'
            url = "http://jinfans.top/others/iotbot/bot_setu_image/hentai/image/" + name
            action.send_friend_pic_msg(ctx.FromUin, url)


