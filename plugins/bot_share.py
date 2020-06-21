# -*- coding: utf-8 -*-
from iotbot import GroupMsg, Action
from util import configuration

# 分享内容
from util.network.request import get_html


def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != configuration.qq:
        action = Action(configuration.qq)
        if ctx.MsgType == 'TextMsg':
            command = ctx.Content.split(' ')
            if command[0] == "歌":
                # TODO: get these long xml into `res/xml` folder
                content = "\u003c?xml version='1.0' encoding='UTF-8' standalone='yes'?\u003e\u003cmsg templateID=\"123\" url=\"https://i.y.qq.com/v8/playsong.html?platform=11\u0026amp;appshare=android_qq\u0026amp;appversion=9160007\u0026amp;hosteuin=oKSioe6k7e-kNn**\u0026amp;songmid=000hqNCg4BrAPC\u0026amp;type=0\u0026amp;appsongtype=1\u0026amp;_wv=1\u0026amp;source=qq\u0026amp;ADTAG=qfshare\" serviceID=\"1\" action=\"\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[分享]真的爱你\" flag=\"0\"\u003e\u003citem layout=\"2\"\u003e\u003cpicture cover=\"http://y.gtimg.cn/music/photo_new/T002R150x150M000003DrnLc0xJRE5_1.jpg\"/\u003e\u003ctitle\u003e真的爱你\u003c/title\u003e\u003csummary\u003eBEYOND\u003c/summary\u003e\u003c/item\u003e\u003csource url=\"\" icon=\"\" name=\"QQ音乐\" appid=\"100497308\" action=\"\" actionData=\"\" a_actionData=\"tencent100497308://\" i_actionData=\"\"/\u003e\u003c/msg\u003e"
                print(content)
                action.send_group_xml_msg(ctx.FromGroupId, content)
            if command[0] == "知乎":
                content = "\u003c?xml version='1.0' encoding='UTF-8' standalone='yes'?\u003e\u003cmsg templateID=\"123\" url=\"http://www.zhihu.com/question/401832549?utm_source=qq\u0026amp;utm_medium=social\u0026amp;utm_oi=1139804641683505152\" serviceID=\"1\" action=\"web\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[QQ小程序]知乎问答：如何看待北京将应急响应级别提升为二级？对日常生活有什么影响？\" flag=\"0\"\u003e\u003citem layout=\"2\"\u003e\u003cpicture cover=\"https://pic1.zhimg.com/v2-b3b480f4b1d15bcd24182f96261334b6.jpg\"/\u003e\u003ctitle\u003e知乎问答：如何看待北京将应急响应级别提升为二级？对日常生活有什么影响？\u003c/title\u003e\u003csummary\u003e来自话题「北京」，已有 947 个回答，3701 人关注\u003c/summary\u003e\u003c/item\u003e\u003csource url=\"http://www.zhihu.com/question/401832549?utm_source=qq\u0026amp;utm_medium=social\u0026amp;utm_oi=1139804641683505152\" icon=\"https://i.gtimg.cn/open/app_icon/00/49/07/01/100490701_100_m.png\" name=\"知乎问答：如何看待北京将应急响应级别提升为二级？对日常生活有什么影响？\" appid=\"0\" action=\"web\" actionData=\"\" a_actionData=\"tencent0://\" i_actionData=\"\"/\u003e\u003c/msg\u003e"
                print(content)
                action.send_group_xml_msg(ctx.FromGroupId, content)
            if command[0] == "点歌":
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
