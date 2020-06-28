# -*- coding: utf-8 -*-
from iotbot import GroupMsg, FriendMsg, Action
from util import configuration


# setu!
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "setu":

                if len(command) == 2:
                    execute = command[1]
                else:
                    execute = "drawings"

                url = "http://jinfans.top/setu/latest/view/random?type=" + execute
                action.send_group_pic_msg(ctx.FromGroupId, execute, picUrl=url)


def receive_friend_msg(ctx: FriendMsg):
    if ctx.FromUin != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "setu":

                if len(command) == 2:
                    execute = command[1]
                else:
                    execute = "hentai"

                url = "http://jinfans.top/setu/latest/view/random?type=" + execute
                action.send_friend_pic_msg(ctx.FromUin, execute, picUrl=url)
