# HTTP Server
基础URL : http://jinfans.top/iotbot/

POST : 
- fromId : 管理员账户
- passwd : 管理员密码（经过md5加密后）
- content : 指令

配置文件 : config.json, app_auth 列表储存："fromId:passwd" 



## 命令
- refresh : 更新插件，返回 str : “插件已刷新”  
- test : 测试，返回测试图片url
- blacklist : 黑名单操作，返回 str  [GET:fromGroupId]
- param : 插件参数设置，返回 str     [GET:fromGroupId]


