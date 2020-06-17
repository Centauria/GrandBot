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


def xml_get_music163(key):
    xml = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID=\"123\" "
    xml += " url=\"https://i.y.qq.com/v8/playsong.html?platform=11\u0026amp;appshare=android_qq\u0026amp;appversion=9160007\u0026amp;hosteuin=oKSioe6k7e-kNn**\u0026amp;songmid=0024cxzk0Xj4wh\u0026amp;type=0\u0026amp;appsongtype=1\u0026amp;_wv=1\u0026amp;source=qq\u0026amp;sharefrom=gedan\u0026amp;from_id=7362032691\u0026amp;from_idtype=0\u0026amp;from_name=dW5kZWZpbmVk\u0026amp;ADTAG=qfshare\""
    xml += " serviceID=\"1\" action=\"\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[分享]光年之外\" flag=\"0\"><item layout=\"2\"> "
    xml += " <picture cover=\"http://y.gtimg.cn/music/photo_new/T002R150x150M000001HGENg0BvGoH_2.jpg\"/> "
    xml += " <title>光年之外</title><summary>文慧如/邱锋泽</summary> "
    xml += " </item><source url=\"\" icon=\"\" name=\"QQ音乐\" appid=\"100497308\" action=\"\" actionData=\"\" a_actionData=\"tencent100497308://\" i_actionData=\"\"/></msg>"
    return xml