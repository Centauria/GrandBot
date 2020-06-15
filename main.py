# -*- coding: utf-8 -*-
from iotbot import IOTBOT, GroupMsg, Action

bot = IOTBOT(1738317487)
action = Action(bot)

@bot.on_group_msg
def group(ctx: GroupMsg):
    print(f"""{ctx.FromNickName}在{ctx.MsgTime}的时候，发了一个类型是{ctx.MsgType}的消息，内容为：
{ctx.Content}""")
    print(ctx.get('CurrentQQ'))
    action.send_friend_text_msg(ctx.FromUin, '1')

@bot.on_friend_msg
def friend(ctx: FriendMsg):
    action.send_friend_text_msg(ctx.FromUin, '1')

bot.run()
