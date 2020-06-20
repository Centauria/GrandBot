# -*- coding: utf-8 -*-
import requests


def get_html(url):
    kv = {
        "User-agent": "Mozilla/5.0"  # 模拟浏览器
    }
    try:
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except:
        return "ERROR"