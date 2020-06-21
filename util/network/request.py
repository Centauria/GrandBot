# -*- coding: utf-8 -*-
import time
import requests
import logging
from logging import Logger
from requests import HTTPError

trial_num = 60
user_agent = {
    'Mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/83.0.4103.61 Safari/537.36',
    'Rpi': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Raspbian Chromium/78.0.3904.108 '
           'Chrome/78.0.3904.108 Safari/537.36',
    'Firefox': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
    'Chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/80.0.3987.106 Safari/537.36'
}
headers_img = {
    'Host': 'gchat.qpic.cn',
    'Proxy-Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': user_agent['Mac'],
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'If-Modified-Since': 'Mon, 08 Jun 2020 17:42:54 GMT'
}
logger = Logger('Network Logger', level=logging.INFO)


def get_img(url: str):
    r = None
    for i in range(trial_num):
        try:
            logger.info(f'Get url: {url}')
            logger.info(f'Trial {i}')
            r = requests.get(url, headers=headers_img, timeout=2)
        except HTTPError as e:
            logger.error(f'Trial {i} failed.')
            time.sleep(1)
        finally:
            if r is not None:
                return r
    return r


def get_html(url):
    kv = {
        "User-agent": user_agent['Mac']  # 模拟浏览器
    }
    r = None
    try:
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except HTTPError as e:
        logger.error(e)
    return r


def get_html_text(url):
    r = get_html(url)
    return r.text if r else None


def get_html_url(url):
    kv = {
        "User-agent": user_agent['Edge']
    }
    r = None
    try:
        r = requests.head(url, timeout=30, headers=kv)
        return r.headers['Location']
    except HTTPError as e:
        logger.error(e)
    return r
