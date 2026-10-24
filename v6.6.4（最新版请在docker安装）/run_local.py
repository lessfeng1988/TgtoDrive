"""本地运行 TgtoDrive v6.6.4（不使用 Docker）。

用法：
    ..\\..\\.venv-tgtodrive\\Scripts\\python.exe run_local.py

环境变量：
    SKIP_123_LOGIN=1   不登录 123 网盘，只启动 Web 面板与调度框架（没有账号时用）

说明：
    旧版在 __main__ 入口处会向 Telegram 频道校验置顶消息版本号（newest_id=47），
    版本不匹配就无限提示更新。源码现已支持 TGTO123_SKIP_VERSION_CHECK=1 跳过该校验，
    直接 `python tgto123.py` 即可；本脚本用 __mp_main__ 方式加载只是为了保留原版的
    模块级初始化（日志、天翼云盘客户端）并便于注入本地调试用的替身。
"""

import os
import runpy

import telebot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

os.environ.setdefault("TGTO123_SKIP_VERSION_CHECK", "1")

# 旧版启动时会联网设置 Bot 命令菜单，网络不通会卡在 30 秒重试循环里
telebot.TeleBot.set_my_commands = lambda self, *args, **kwargs: None

module = runpy.run_path(os.path.join(BASE_DIR, "tgto123.py"), run_name="__mp_main__")

# 123 登录失败会直接抛异常让主线程退出，无账号时用空客户端占位
if os.getenv("SKIP_123_LOGIN") == "1":
    module["main"].__globals__["init_123_client"] = lambda retry=False: None

module["main"]()
