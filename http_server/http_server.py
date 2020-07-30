# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from admin.admin_refresh import admin_refresh
from admin.admin_test import admin_test
from admin.admin_blacklist import admin_blacklist, admin_blacklist_find
from admin.admin_param import admin_param, admin_param_find
from .http_auth import *
from .http_get_bots import *
from .http_get_groups import *
from .http_get_commands import *

app = Flask(__name__)


# 需要引用bot的功能，在此处定义，在main引用
def http_refresh_raw(bot, content, fromId):
	return admin_refresh(bot, 0, content, fromId)


# 无需引用bot的功能
@app.route('/', methods=['GET', 'POST'])
def http_hello():
	return {"result": True, "content": "欢迎来到 IOTBOT app 后台！"}


@app.route('/login', methods=['POST'])
def http_login():
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		return {"result": True, "content": str(post_data["fromId"])}
	else:
		return {"result": False, "content": auth_result}


@app.route('/avatar', methods=['GET'])
def http_avatar():
	get_data = request.args
	if "user" in get_data:
		url = ""
		with open("res/json/admin_avatar_url.json", 'r') as load_file:
			avatar_list = json.load(load_file)
		for bot in avatar_list:
			if bot["account"] == get_data["user"]:
				url = bot["avatar_url"]

		# 直接返回图片
		if url == "":
			return
		else:
			with open("res/image/" + url, 'rb') as f:
				image = f.read()
			resp = Response(image, mimetype="image/jpeg")
			return resp
	else:
		return


@app.route('/botslist', methods=['POST'])
def http_botslist():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "page" not in get_data or "page_size" not in get_data:
			return {"result": False, "content": "命令错误：参数错误"}
		page = int(get_data["page"])
		page_size = int(get_data["page_size"])
		list = botsList()
		start = (page - 1) * page_size
		end = min(page * page_size, len(list))

		return {"result": True, "content": list[start:end]}
	else:
		return {"result": False, "content": auth_result}


@app.route('/groupslist', methods=['POST'])
def http_groupslist():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "page" not in get_data or "page_size" not in get_data or "content" not in post_data:
			return {"result": False, "content": "命令错误：参数错误"}
		page = int(get_data["page"])
		page_size = int(get_data["page_size"])
		list = groupsList(post_data["content"])
		start = (page - 1) * page_size
		end = min(page * page_size, len(list))

		return {"result": True, "content": list[start:end]}
	else:
		return {"result": False, "content": auth_result}


@app.route('/commandslist', methods=['POST'])
def http_commandslist():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "page" not in get_data or "page_size" not in get_data:
			return {"result": False, "content": "命令错误：参数错误"}

		page = int(get_data["page"])
		page_size = int(get_data["page_size"])
		list = commandsList()
		start = (page - 1) * page_size
		end = min(page * page_size, len(list))

		return {"result": True, "content": list[start:end]}
	else:
		return {"result": False, "content": auth_result}


@app.route('/test', methods=['POST'])
def http_test():
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "content" in post_data:
			result = admin_test(0, post_data["content"], post_data["fromId"])
			if result:
				return {"result": True, "content": result}
			else:
				return {"result": False, "content": "命令错误：执行失败"}
		else:
			return {"result": False, "content": "命令错误：请提交命令内容"}
	else:
		return {"result": False, "content": auth_result}


@app.route('/blacklist', methods=['POST'])
def http_blacklist():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "content" in post_data and "fromGroupId" in get_data:
			if post_data["content"] == ".blacklist find":

				if "page" not in get_data or "page_size" not in get_data:
					return {"result": False, "content": "命令错误：参数错误"}

				page = int(get_data["page"])
				page_size = int(get_data["page_size"])
				return admin_blacklist_find(int(get_data["fromGroupId"]), page, page_size)
			else:
				result = admin_blacklist(0, post_data["content"], int(get_data["fromGroupId"]))
				if result:
					return result
				else:
					return {"result": False, "content": "命令错误：非法命令"}
		else:
			return {"result": False, "content": "命令错误：请提交命令内容"}
	else:
		return {"result": False, "content": auth_result}


@app.route('/param', methods=['POST'])
def http_param():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "content" in post_data and "fromGroupId" in get_data:
			if post_data["content"] == ".param find":

				if "page" not in get_data or "page_size" not in get_data:
					return {"result": False, "content": "命令错误：参数错误"}

				page = int(get_data["page"])
				page_size = int(get_data["page_size"])
				return admin_param_find(int(get_data["fromGroupId"]), page, page_size)
			else:
				result = admin_param(0, post_data["content"], int(get_data["fromGroupId"]))
				if result:
					return result
				else:
					return {"result": False, "content": "命令错误：非法命令"}
		else:
			return {"result": False, "content": "命令错误：请提交命令内容"}
	else:
		return {"result": False, "content": auth_result}
