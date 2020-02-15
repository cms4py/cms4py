import os

SERVER_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.join(SERVER_ROOT, "app")
CONTROLLERS_ROOT = os.path.join(APP_ROOT, "controllers")
STATIC_FILES_ROOT = os.path.join(APP_ROOT, "static")
VIEWS_ROOT = os.path.join(APP_ROOT, 'views')

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
