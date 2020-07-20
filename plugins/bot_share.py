# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration

# 分享内容
from util.network.request import get_html
from util.plugins.control import PluginControl


def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:

        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "点歌":

                # check
                plugin = PluginControl()
                if not plugin.check("分享", ctx.FromGroupId):
                    return

                if len(command) == 2:
                    content = xml_get_qq(command[1])
                    print(content)
                    action.send_group_xml_msg(ctx.FromGroupId, content)
                if len(command) == 3:
                    content = xml_get_qq(command[1], int(command[2]))
                    print(content)
                    action.send_group_xml_msg(ctx.FromGroupId, content)


# 获得信息 info["song_name", "singer_name", "url", "image_url"]
def info_get_qq(text):
    # TODO: use `re` package for shorter code
    info = []

    song_start = text.find("\"songname\"") + 12
    song_finish = text.find("\",\"", song_start)
    info.append(text[song_start:song_finish])

    singer_start = text.find("\"name\"") + 8
    singer_finish = text.find("\",\"", singer_start)
    info.append(text[singer_start:singer_finish])

    url_start = text.find("\"songmid\"") + 11
    url_finish = text.find("\",\"", url_start)
    info.append(text[url_start:url_finish])

    album_start = text.find("\"albumname\"") + 13
    album_finish = text.find("\",\"", album_start)
    info.append(text[album_start:album_finish])

    return info


def info_image_get_qq(text):
    # TODO: use `re` package for shorter code
    song_start = text.find("\"albumPic\"") + 12
    song_finish = text.find("\",\"", song_start)

    return text[song_start:song_finish]


# TODO: get these long xml into `res/xml` folder
def xml_get_qq(key, num=1):
    info = info_get_qq(
        get_html("https://c.y.qq.com/soso/fcgi-bin/client_search_cp?t=0&p=" + f"""{num}""" + "&n=1&w=" + key).text)
    info.append(
        info_image_get_qq(get_html("https://c.y.qq.com/soso/fcgi-bin/client_search_cp?t=8&p=1&n=1&w=" + info[3]).text))
    xml = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID=\"123\" "
    xml += " url=\"https://i.y.qq.com/v8/playsong.html?platform=11&amp;songmid=" + f"""{info[2]}\" """
    xml += " serviceID=\"1\" action=\"web\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[分享]" + f"""{info[0]}""" + "\" flag=\"0\"><item layout=\"2\"> "
    xml += " <picture cover=\"" + f"""{info[4]}""" + "\"/> "
    xml += " <title>" + f"""{info[0]}""" + "</title><summary>" + f"""{info[1]}""" + "</summary> "
    xml += " </item><source url=\"\" icon=\"\" name=\"QQ音乐\" appid=\"100497308\" action=\"\" actionData=\"\" a_actionData=\"tencent100497308://\" i_actionData=\"\"/></msg>"
    return xml
