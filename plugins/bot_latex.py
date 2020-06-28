# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration

from util.network.request import post


# 输入 “latex 关键字”，回显公式图片
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':

            command = ctx.Content.split(' ', 1)
            if command[0] == "latex" and len(command) > 1:
                latex_content = command[1].replace("\\", "\\\\")
                url = 'https://quicklatex.com/latex3.f'
                data = {"formula": latex_content, "fcolor": "000000", "fsize": "17px", "mode": "0", "out": "1", "remhost": "quicklatex.com"}
                response = post(url, data)

                content = response.text.split("\r\n")[1]
                if content[0] == "0":
                    pic_url = content[1].split(' ')[0]
                    action.send_group_pic_msg(ctx.FromGroupId, picUrl=pic_url)
                else:
                    action.send_group_text_msg(ctx.FromGroupId, "无法识别公式！")
