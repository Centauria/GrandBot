# -*- coding: utf-8 -*-
from iotbot import IOTBOT, GroupMsg, FriendMsg, Action

from util import configuration

bot = IOTBOT(configuration.qq, use_plugins=True)
action = Action(bot)


@bot.on_friend_msg
def friend(ctx: FriendMsg):
    print(f"""内容为：{ctx.Content}""")
    print(ctx.get('CurrentQQ'))
    action.send_friend_text_msg(ctx.FromUin, ctx.Content)


bot.run()
