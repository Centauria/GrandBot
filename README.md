# GrandBot
基于python-IOTBOT的一些沙雕Python插件

功能：

- [x] 本地聊天记录
- [x] 概率复读
- [x] 概率回复
- [x] 百度
- [x] 防撤回
- [x] 色图！
- [x] QQ音乐搜索
- [x] 计时器与闹钟
- [ ] 语音合成
- [ ] 色图识别
- [ ] 表情包识别

使用：

```shell script
python main.py
```

在运行之前请确保根目录下有有效的`config.conf`文件。文件格式请参照`example.conf`。
如果要使用`config.conf`中的配置，请在python代码中加入

```python
from util.config import configuration
```

即可。