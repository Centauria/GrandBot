# -*- coding: utf-8 -*-
import os
import requests
from iotbot import GroupMsg, Action
from util import configuration


# 输入 “百度 关键字”，回显百科内容
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg' and judge_msg(ctx.Content, "百度"):
            baidu_content = get_text(ctx.Content[3:])
            print(baidu_content)
            action.send_group_text_msg(
                ctx.FromGroupId,
                os.linesep.join(baidu_content)
            )


# 命令判断
def judge_msg(msg, key):
    for i in range(len(key)):
        if msg[i] != key[i]:
            return False
    return True


# 获取html
def get_html_text(url):
    kv = {
        "User-agent": "Mozilla/5.0"  # 模拟浏览器
    }
    try:
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "ERROR"


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
    text = []
    url = "https://baike.baidu.com/search/word?word=" + key
    s = get_html_text(url)

    start = s.find("<div class=\"lemma-summary\" label-module=\"lemmaSummary\">")
    finish = s.find("<div class=\"lemmaWgt-promotion-leadPVBtn\">")

    index = []
    k = s.find("<div class=\"para\" label-module=\"para\">", start)
    i = 0
    while k != -1 and k < finish:
        index.append(k + 38)
        k = s.find("<div class=\"para\" label-module=\"para\">", index[i])
        i = i + 1

    for i in range(len(index)):
        if i == len(index) - 1:
            text.append(s[index[i]:finish - 14])
        else:
            text.append(s[index[i]:index[i + 1] - 44])

    for i in range(len(text)):
        text[i] = remove_between(text[i], '<', '>')
        text[i] = remove_between(text[i], '[', ']')
        text[i] = text[i].replace("&nbsp;", '')
        text[i] = text[i].replace("\n", '')

    return text


key = "中国"
print(get_text(key))
