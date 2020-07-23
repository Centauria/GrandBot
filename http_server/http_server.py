# -*- coding: utf-8 -*-
from flask import Flask, request
from admin.admin_refresh import admin_refresh
from admin.admin_test import admin_test
from admin.admin_blacklist import admin_blacklist
from admin.admin_param import admin_param
from .http_auth import *

app = Flask(__name__)


# 需要引用bot的功能，在此处定义，在main引用
def http_refresh_raw(bot, content, fromId):
	return admin_refresh(bot, 0, content, fromId)


# 无需引用bot的功能
@app.route('/', methods=['GET', 'POST'])
def http_hello():
	return "欢迎来到 IOTBOT app 后台！"


@app.route('/test', methods=['POST'])
def http_test():
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "content" in post_data:
			result = admin_test(0, post_data["content"], post_data["fromId"])
			if result:
				return result
			else:
				return "命令错误：执行失败"
		else:
			return "命令错误：请提交命令内容"
	else:
		return auth_result


@app.route('/blacklist', methods=['POST'])
def http_blacklist():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "content" in post_data and "fromGroupId" in get_data:
			result = admin_blacklist(0, post_data["content"], int(get_data["fromGroupId"]))
			if result:
				return result
			else:
				return "命令错误：非法命令"
		else:
			return "命令错误：请提交命令内容"
	else:
		return auth_result


@app.route('/param', methods=['POST'])
def http_param():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "content" in post_data and "fromGroupId" in get_data:
			result = admin_param(0, post_data["content"], int(get_data["fromGroupId"]))
			if result:
				return result
			else:
				return "命令错误：执行失败"
		else:
			return "命令错误：请提交命令内容"
	else:
		return auth_result
