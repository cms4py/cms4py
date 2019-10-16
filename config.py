import os
import sys

APP_ROOT = os.path.dirname(__file__)
sys.path.append(APP_ROOT)

"""
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""
LOG_LEVEL = 10

PORT = 8000
APP_NAME = "cms4py"
APP_VERSION = "2019.10.12"
STATIC_FILES_ROOT = os.path.join(APP_ROOT, "cms4py", "static")
STATIC_FILES_URL_PATH = "static"
DEFAULT_STATIC_FILE_NAME = "index.html"

DB_URI = "mysql://root:example@db/cms4py"
DB_POOR_SIZE = 10
DB_FOLDER = os.path.join(APP_ROOT, "cms4py", "databases")
DB_MIGRATE = False
DB_USE_BIGINT_ID = True

"""
If you want to use secure cookies to store the session id, change this value
"""
COOKIE_SECRET = None
CMS4PY_SESSION_ID_KEY = "cms4py_session_id"

TRANSLATIONS_FOLDER = os.path.join(APP_ROOT, "cms4py", "languages")
TEMPLATES_FOLDER = os.path.join(APP_ROOT, "cms4py", "templates")
