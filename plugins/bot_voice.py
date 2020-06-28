# -*- coding: utf-8 -*-
import pyttsx3
import time
import string
import random
from iotbot import GroupMsg, Action
from util import configuration


# TODO: it can't work on linux
# 输入文字，以语音形式发送
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "说话" and len(command) >= 2:
                msg = command[1]
                path = '../voice/' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + \
                       ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '.mp3'
                volume = 1.0
                rate = 100
                voice = 0
                for i in range(len(command) - 2):
                    if command[i + 2][:7] == 'volume=':
                        volume = command[i + 2].lstrip('volume=')
                        try:
                            volume = float(volume)
                        except:
                            action.send_group_text_msg(ctx.FromGroupId, "参数:volume 有误！")
                    elif command[i + 2][:5] == 'rate=':
                        rate = command[i + 2].lstrip('rate=')
                        try:
                            rate = int(rate)
                        except:
                            action.send_group_text_msg(ctx.FromGroupId, "参数:rate 有误！")
                    elif command[i + 2][:6] == 'voice=':
                        voice = command[i + 2].lstrip('voice=')
                        try:
                            voice = int(voice)
                        except:
                            action.send_group_text_msg(ctx.FromGroupId, "参数:voice 有误！")
                save(msg, path, volume, rate, voice)
                action.send_friend_voice_msg(ctx.FromGroupId, path)


def save(msg, path, volume=1.0, rate=100, voice=0):
    engine = pyttsx3.init()
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)
    engine.save_to_file(msg, path)
    engine.runAndWait()
    engine.stop()
