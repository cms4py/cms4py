import os

SERVER_VERSION = '2020.02.15'
SERVER_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.join(SERVER_ROOT, "app")
CONTROLLERS_ROOT = os.path.join(APP_ROOT, "controllers")
STATIC_FILES_ROOT = os.path.join(APP_ROOT, "static")
VIEWS_ROOT = os.path.join(APP_ROOT, 'views')
LANGUAGES_ROOT = os.path.join(APP_ROOT, 'languages')
LANGUAGE = None  # "zh-CN", "en-US"

SERVER_NAME = b'cms4py'
APP_NAME = "cms4py"

"""
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""
LOG_LEVEL = 10

DEFAULT_CONTROLLER = "default"
DEFAULT_ACTION = 'index'
APP_VERSION = '2020.02.15'

GLOBAL_CHARSET = 'utf-8'
CMS4PY_SESSION_ID_KEY = b"cms4py_session_id"
