# -*- coding: utf-8 -*-
import random
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration


# setu!
def receive_group_msg(ctx: GroupMsg):
    num = {"hentai": 4461, "drawings": 15566}
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "setu":

                if len(command) == 2:
                    execute = command[1]
                else:
                    execute = "hentai"

                for c in num:
                    if c == execute:
                        no = random.randint(1, num[c])
                        name = execute + "{:0>5d}".format(no) + '.png'
                        url = "http://jinfans.top/others/iotbot/bot_setu_image/hentai/image/" + name
                        action.send_group_pic_msg(ctx.FromGroupId,  picUrl=url)


def receive_friend_msg(ctx: FriendMsg):
    num = {"hentai": 4461, "drawings": 15566}
    if ctx.FromUin != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "setu":

                if len(command) == 2:
                    execute = command[1]
                else:
                    execute = "hentai"

                for c in num:
                    if c == execute:
                        no = random.randint(1, num[c])
                        name = execute + "{:0>5d}".format(no) + '.png'
                        url = "http://jinfans.top/others/iotbot/bot_setu_image/hentai/image/" + name
                        action.send_group_pic_msg(ctx.FromGroupId, picUrl=url)


