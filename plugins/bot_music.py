# -*- coding: utf-8 -*-
import requests
from iotbot import GroupMsg, Action
from util import configuration


# 输入 “百度 关键字”，回显百科内容
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg' and ctx.Content == "歌":
            print("Music Send Begin")
            content = "\u003c?xml version='1.0' encoding='UTF-8' standalone='yes'?\u003e\u003cmsg templateID=\"123\" url=\"http://music.163.com/song/41672085/?userid=310189939\" serviceID=\"1\" action=\"\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[分享]星雨之夜\" flag=\"0\"\u003e\u003citem layout=\"2\"\u003e\u003cpicture cover=\"https://cpic.url.cn/v1/9e85h525uohcnsda7066pspia3o3hp8d4of7g6dnf01cq3bjbjr20lmfsmoo539mvu1uhesaj5hdvherdhbmedtobp76eak940f6pce0u338ace7ill106n9hfkkgvaa/bulps27rab4hblqf1sch7rk5o3fe6t09r9mt9r99cocnc79v7v00\"/\u003e\u003ctitle\u003e星雨之夜\u003c/title\u003e\u003csummary\u003e心华/ilem\u003c/summary\u003e\u003c/item\u003e\u003csource url=\"\" icon=\"\" name=\"网易云音乐\" appid=\"100495085\" action=\"\" actionData=\"\" a_actionData=\"tencent100495085://\" i_actionData=\"\"/\u003e\u003c/msg\u003e[分享]星雨之夜\n心华/ilem\nhttp://music.163.com/song/41672085/?userid=310189939\n来自: 网易云音乐"
            send_group_music_msg(action, ctx.FromGroupId, content)

def send_group_music_msg(action, toUser: int, content, atUser=0, timeout=5, **kwargs) -> dict:
    """发送群Xml类型信息"""
    data = {
        "toUser": toUser,
        "sendToType": 2,
        "sendMsgType": "XmlMsg",
        "content": content,
        "groupid": 0,
        "atUser": atUser
    }
    print("data Formatted")
    return action.baseSender('POST', 'SendMsg', data, timeout, **kwargs)


