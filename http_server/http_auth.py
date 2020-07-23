# -*- coding: utf-8 -*-
from util import configuration
import hashlib


# auth, POST内需要fromId、passwd(md5)
# 0: auth ok ; 1: auth false ; 2: command wrond
def auth(post_data):
	if "fromId" in post_data and "passwd" in post_data:
		for user in configuration.app_auth:
			auth_raw = str(user).split(":", 1)
			if auth_raw[0] == post_data["fromId"] and hashlib.md5(auth_raw[1].encode(encoding='UTF-8')).hexdigest() == \
					post_data["passwd"]:
				return 0
		return "管理员认证失败"
	else:
		return "命令错误：请提交管理员账户和密码"
