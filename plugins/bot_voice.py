# -*- coding: utf-8 -*-
import os
import requests
from iotbot import GroupMsg, Action
from util import configuration


# 输入 “百度 关键字”，回显百科内容
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            if ctx.Content == "说话":
                action.send_group_voice_msg(ctx.FromGroupId, "http://grouptalk.c2c.qq.com/?ver=0\u0026rkey=3062020101045b30590201010201010204679c9eaf042439306a336f6f4e45517536386638785574717273666a4930586d6e6a4441313332766b7a02045eec8b88041f0000000866696c6574797065000000013100000005636f64656300000001310400\u0026filetype=1\u0026voice_codec=1")