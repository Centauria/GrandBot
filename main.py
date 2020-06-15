# -*- coding: utf-8 -*-
from iotbot import IOTBOT, GroupMsg

bot = IOTBOT(1738317487)


@bot.on_group_msg
def group(ctx: GroupMsg):
    print(f"""
{ctx.FromNickName}在{ctx.MsgTime}的时候，发了一个类型是{ctx.MsgType}的消息，内容为：
{ctx.Content}""")
    print(ctx.get('CurrentQQ'))


bot.run()
