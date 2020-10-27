
import os

# 服务器版本
SERVER_VERSION = '2020.02.15'
# 服务器根目录
SERVER_ROOT = os.path.dirname(os.path.abspath(__file__))
# 应用所在目录的目录名
APP_DIR_NAME = "app"
# 应用根目录
APP_ROOT = os.path.join(SERVER_ROOT, APP_DIR_NAME)
# 控制器所在的目录的目录名
CONTROLLERS_DIR_NAME = "controllers"
# 控制器所在目录
CONTROLLERS_ROOT = os.path.join(APP_ROOT, CONTROLLERS_DIR_NAME)
# 静态文件根目录
STATIC_FILES_ROOT = os.path.join(APP_ROOT, "static")
# 模板文件根目录
VIEWS_ROOT = os.path.join(APP_ROOT, 'views')
# 语言文件根目录
LANGUAGES_ROOT = os.path.join(APP_ROOT, 'languages')
# Socket.IO 文件所在目录
SOCKET_IO_DIR_NAME = "sio"
# 默认语言
LANGUAGE = None  # "zh-CN", "en-US"

# 服务器名称
SERVER_NAME = 'cms4py'

# 应用名称
APP_NAME = "cms4py"

"""
日志级别

CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""
LOG_LEVEL = 10

# 在用户未指定控制器的情况下由该默认控制器接受请求
DEFAULT_CONTROLLER = "default"
# 在用户未指定控制器函数的情况下由该动作（action）接受请求
DEFAULT_ACTION = 'index'

# 应用版本
APP_VERSION = '2020.02.15'

# 全局编码方式
GLOBAL_CHARSET = 'utf-8'

# 在 Cookie 中存储 Session ID 所使用的键名
CMS4PY_SESSION_ID_KEY = b"cms4py_session_id"
