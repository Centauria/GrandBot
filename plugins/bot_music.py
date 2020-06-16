# -*- coding: utf-8 -*-
import requests
from iotbot import GroupMsg, Action
from util import configuration


# 输入 “百度 关键字”，回显百科内容
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg' and ctx.Content == "歌":
            content = "\u003c?xml version='1.0' encoding='UTF-8' standalone='yes'?\u003e\u003cmsg templateID=\"123\" url=\"http://music.163.com/song/551339691/?userid=310189939\" serviceID=\"1\" action=\"\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[分享]Euphoria\" flag=\"0\"\u003e\u003citem layout=\"2\"\u003e\u003cpicture cover=\"https://cpic.url.cn/v1/9e85h525uohcnsda7066pspia0at5nkoprao8qec2f2iljd2ed9l5fjud4d5fp6ietqrn54p3k5eu4ask1s53j9hdsdc9l9mqo2cbrm9s60iqdu62nla5cek83oabnqo/bulps27rab4hblqf1sch7rk5o3fe6t09r9mt9r99cocnc79v7v00\"/\u003e\u003ctitle\u003eEuphoria\u003c/title\u003e\u003csummary\u003eじん/IA\u003c/summary\u003e\u003c/item\u003e\u003csource url=\"\" icon=\"\" name=\"网易云音乐\" appid=\"100495085\" action=\"\" actionData=\"\" a_actionData=\"tencent100495085://\" i_actionData=\"\"/\u003e\u003c/msg\u003e[分享]Euphoria\nじん/IA\nhttp://music.163.com/song/551339691/?userid=310189939\n来自: 网易云音乐"
            action.send_group_xml_msg(ctx.FromGroupId, content)




