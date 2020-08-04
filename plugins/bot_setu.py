# -*- coding: utf-8 -*-
import json

from iotbot import GroupMsg, FriendMsg, Action

from util import configuration
from util.network.request import get_html_text
from util.plugins.control import PluginControl


# setu!
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:

        # check
        plugin = PluginControl()
        if not plugin.check("setu", ctx.FromUserId, ctx.FromGroupId):
            return

        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "setu":

                if len(command) == 2:
                    execute = command[1]
                else:

                    # param
                    param = plugin.find_one("setu", ctx.FromGroupId)["param"]
                    execute = param["default"]

                id_url = "http://jinfans.top/setu/latest/view/random?type=" + execute
                id_image = get_html_text(id_url)
                id_json = json.loads(id_image)
                url = "http://jinfans.top/setu/latest/view/direct/" + id_json["_id"]
                action.send_group_pic_msg(ctx.FromGroupId, content=execute, picUrl=url)


def receive_friend_msg(ctx: FriendMsg):
    setu_allow = False
    if ctx.FromUin != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "setu":
                if setu_allow:
                    if len(command) == 2:
                        execute = command[1]
                    else:
                        execute = "drawings"

                    id_url = "http://jinfans.top/setu/latest/view/random?type=" + execute
                    id_image = get_html_text(id_url)
                    id_json = json.loads(id_image)
                    url = "http://jinfans.top/setu/latest/view/direct/" + id_json["_id"]
                    action.send_friend_pic_msg(ctx.FromUin, content=execute, picUrl=url)
                else:
                    action.send_friend_text_msg(ctx.FromUin, content='你在想🍑')
