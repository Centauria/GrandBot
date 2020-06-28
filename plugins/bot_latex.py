# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration
import re
from util.network.request import post


# 输入 “latex 关键字”，回显公式图片
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':

            command = ctx.Content.split(' ', 1)
            if command[0] == "latex" and len(command) > 1:
                latex_content = command[1]
                url = 'https://quicklatex.com/latex3.f'

                data = {"formula": transfer_spacing(latex_content), "fcolor": "000000", "fsize": "100px", "mode": "0", "out": "1", "remhost": "quicklatex.com"}
                response = post(url, data)
                content = response.text.split("\r\n")
                if content[0] == "0":
                    pic_url = content[1].split(' ')[0]
                    print(pic_url)
                    action.send_group_pic_msg(ctx.FromGroupId, picUrl=pic_url, timeout=10)
                else:
                    action.send_group_text_msg(ctx.FromGroupId, "无法识别公式！")


#将空格转义
def transfer_spacing(latex_content):
    c_list = [i.start() for i in re.finditer(' ', latex_content)]
    new_content = list(latex_content)
    for i in range(len(c_list)):
        new_content.insert(c_list[i] + i, '\\')
    return "".join(new_content)