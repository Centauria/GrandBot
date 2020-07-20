# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration

from util.network.request import get_html_url, get_html
from util.plugins.control import PluginControl


# 输入 “百度 关键字”，回显百科内容
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:

        # check
        plugin = PluginControl()
        if not plugin.check("百度", ctx.FromGroupId):
            return

        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':

            command = ctx.Content.split(' ')
            if command[0] == "百度" and len(command) > 1:
                baidu_content = get_text(command[1])
                url_new = "https:" + get_html_url("https://baike.baidu.com/search/word?word=" + command[1])
                print("内容", baidu_content, baidu_content == "")

                if baidu_content == "":
                    action.send_group_text_msg(ctx.FromGroupId, "爷没有搜索到结果！")
                else:
                    if len(command) == 2:
                        action.send_group_text_msg(ctx.FromGroupId, baidu_content[:] + url_new)
                    elif len(command) == 3:
                        try:
                            i = int(command[2])
                        except:
                            action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数！")
                        if i > 0:
                            action.send_group_text_msg(ctx.FromGroupId, baidu_content[:i] + "......\n\n" + url_new)
                        else:
                            action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数！")
                    else:
                        action.send_group_text_msg(ctx.FromGroupId, "爷发现你输入了非法参数！")


# 去除两个符号中间的所有内容
def remove_between(text, f1, f2):
    s1 = text.find(f1)
    s2 = text.find(f2)
    while s1 != -1:
        text = text[:s1] + text[s2 + 1:]
        s1 = text.find(f1)
        s2 = text.find(f2)
    return text


# 获得说明
def get_text(key):
    url = "https://baike.baidu.com/search/word?word=" + key
    html = get_html(url)
    s = html.text

    start = s.find("<div class=\"lemma-summary\" label-module=\"lemmaSummary\">")
    finish = s.find("<div class=\"lemmaWgt-promotion-leadPVBtn\">")

    s = s[start:finish]

    text = s.split("</div>")

    for i in range(len(text)):
        text[i] = remove_between(text[i], '<', '>')
        text[i] = remove_between(text[i], '[', ']')
        text[i] = text[i].replace("&nbsp;", '')
        text[i] = text[i].replace("\n", '')

    string = '\n\n'.join(text)

    return string
