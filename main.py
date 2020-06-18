# -*- coding: utf-8 -*-
from iotbot import IOTBOT, Action, GroupMsg, FriendMsg
import logging

from util import configuration

# logging.basicConfig(level=logging.ERROR)

bot = IOTBOT(configuration.qq, use_plugins=True, plugin_dir='plugins', log_file_path='logs/log',)
action = Action(bot)


@bot.on_group_msg
def on_group_msg(ctx: GroupMsg):
    if ctx.FromUserId in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
        content = ctx.Content.lstrip('.')
        if content == 'refresh':
            bot.refresh_plugins()
            action.send_group_text_msg(ctx.FromGroupId, '插件已刷新')
        elif content == 'test':
            action.send_group_pic_msg(ctx.FromGroupId, 'https://t.cn/A6Am7xYO')
        else:
            action.send_group_text_msg(ctx.FromGroupId, '不要乱发指令啊喂')


@bot.on_friend_msg
def on_friend_msg(ctx: FriendMsg):
    if ctx.FromUin in configuration.admin and ctx.MsgType == 'TextMsg' and ctx.Content[0] == '.':
        content = ctx.Content.lstrip('.')
        if content == 'refresh':
            bot.refresh_plugins()
            action.send_friend_text_msg(ctx.FromUin, '插件已刷新')
        elif content == 'test':
            action.send_friend_pic_msg(ctx.FromUin, content='', picUrl='https://t.cn/A6Am7xYO')
        else:
            action.send_friend_text_msg(ctx.FromUin, '不要乱发指令啊喂')



bot.run()
