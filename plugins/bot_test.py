# -*- coding: utf-8 -*-
import requests
from iotbot import GroupMsg, Action
from util import configuration


# 分享内容
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        print("TESTTTTT")
        if ctx.MsgType == 'XmlMsg':
            print(ctx.Content)
            action.send_group_xml_msg(ctx.FromGroupId, ctx.Content)
