# -*- coding: utf-8 -*-
import requests
from iotbot import GroupMsg, Action
from util import configuration


# 分享内容
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "点歌" and len(command) == 2:
                content = xml_get_music163(command[1])
                action.send_group_xml_msg(ctx.FromGroupId, content)
            else:
                action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数！")

def xml_get_music163(key):
    xml = ""

    return xml