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
DEFAULT_STATIC_FILE_NAME = "index.html"

DB_HOST = "db"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "example"
DB_NAME = "cms4py"
DB_POOR_SIZE = 10

"""
If you want to use secure cookies to store the session id, change this value
"""
COOKIE_SECRET = None
CMS4PY_SESSION_ID_KEY = "cms4py_session_id"

TRANSLATIONS_FOLDER = os.path.join(APP_ROOT, "cms4py", "languages")
TEMPLATES_FOLDER = os.path.join(APP_ROOT, "cms4py", "templates")
