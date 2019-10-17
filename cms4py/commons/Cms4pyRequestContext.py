import os
import uuid, json.decoder
from typing import Optional, Dict, Any, Awaitable

import tornado.escape
import tornado.web
from tornado import httputil

import config
from .URL import URL
from ..db import connect_db
from pydal import DAL


class Cms4pyRequestContext(tornado.web.RequestHandler):

    def __init__(self, application: "tornado.web.Application", request: httputil.HTTPServerRequest,
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self._db = None
        self._session = {}
        self._session_id = None
        self._session_changed = False

    @property
    def db(self) -> DAL:
        return self._db

    @property
    def session(self):
        return self._session

    def set_session(self, key, value):
        self._session[key] = value
        self._session_changed = True

    def get_session(self, key, default_value=None):
        return self._session[key] if key in self._session else default_value

    @property
    def session_id(self):
        return self._session_id

    def prepare(self) -> Optional[Awaitable[None]]:
        self._db = db = connect_db()
        key = config.CMS4PY_SESSION_ID_KEY
        self._session_id = self.get_secure_cookie(key) if config.COOKIE_SECRET else self.get_cookie(key)
        session_record = db(db.session.session_id == self.session_id).select().first()
        if session_record:
            session_str = session_record.session_content
            try:
                self._session = tornado.escape.json_decode(session_str)
            except json.decoder.JSONDecodeError:
                pass
        if not self.session_id or not session_record:
            self._session_id = uuid.uuid4().hex
            if config.COOKIE_SECRET:
                self.set_secure_cookie(key, self.session_id)
            else:
                self.set_cookie(key, self.session_id)
        return super().prepare()

    def get_template_path(self) -> Optional[str]:
        return config.TEMPLATES_FOLDER

    def get_template_namespace(self) -> Dict[str, Any]:
        ns = super().get_template_namespace()
        ns["config"] = config
        ns["path"] = os.path
        ns["URL"] = URL
        ns["session"] = self._session
        return ns

    def on_finish(self) -> None:
        super().on_finish()
        if self._session_changed:
            self.db.session.update_or_insert(
                self.db.session.session_id == self.session_id,
                session_id=self.session_id,
                session_content=tornado.escape.json_encode(self.session)
            )
        self.db.close()

    def has_argument(self, arg_name):
        return arg_name in self.request.query_arguments or arg_name in self.request.body_arguments
