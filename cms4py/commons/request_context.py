import json.decoder
import os
import uuid
from typing import Optional, Dict, Any

import tornado.escape
import tornado.ioloop
import tornado.web
from tornado import httputil

import config
from cms4py.aiomysql_pydal import PyDALCursor
from cms4py.db import DbConnector
from .response import Response
from .url import URL
from . import auth


class RequestContext(tornado.web.RequestHandler):

    def __init__(self, application: "tornado.web.Application", request: httputil.HTTPServerRequest,
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self._db = None
        self._session = {}
        self._session_id = None
        self._session_changed = False
        self._pydal_connection = None
        self._response = Response()

    @property
    def response(self):
        return self._response

    @property
    def db(self) -> PyDALCursor:
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

    async def prepare(self):
        self._pydal_connection = await DbConnector.get_instance().async_dal.acquire()
        await self._pydal_connection.autocommit(True)
        self._db = db = await self._pydal_connection.cursor()

        key = config.CMS4PY_SESSION_ID_KEY
        self._session_id = self.get_secure_cookie(key) if config.COOKIE_SECRET else self.get_cookie(key)
        session_record = (await db(db.session.session_id == self.session_id).select()).first()
        if session_record:
            session_str = session_record.session_content
            try:
                self._session = tornado.escape.json_decode(session_str)
                self.current_user = self.get_session("current_user")
            except json.decoder.JSONDecodeError:
                pass
        if not self.session_id or not session_record:
            self._session_id = uuid.uuid4().hex
            if config.COOKIE_SECRET:
                self.set_secure_cookie(key, self.session_id)
            else:
                self.set_cookie(key, self.session_id)

    def get_template_path(self) -> Optional[str]:
        return config.TEMPLATES_FOLDER

    def set_current_user(self, user):
        """
        If you want to store the current user to session, call this function
        :param user:
        :return:
        """
        if user:
            self.set_session(
                "current_user",
                dict(
                    id=user.id,
                    login_name=user.login_name,
                    email=user.email,
                    phone=user.phone,
                    nickname=user.nickname
                )
            )
        else:
            del self.session["current_user"]
            self._session_changed = True
        self.current_user = user

    def get_template_namespace(self) -> Dict[str, Any]:
        ns = super().get_template_namespace()
        ns["config"] = config
        ns["path"] = os.path
        ns["URL"] = URL
        ns["session"] = self._session
        ns['response'] = self.response
        return ns

    async def cleanup(self):
        if self.db:
            if self._session_changed:
                await self.db.session.update_or_insert(
                    self.db.session.session_id == self.session_id,
                    session_id=self.session_id,
                    session_content=tornado.escape.json_encode(self.session)
                )
            await self.db.close()
        if self._pydal_connection:
            await DbConnector.get_instance().async_dal.release(self._pydal_connection)

    def on_finish(self) -> None:
        super().on_finish()
        tornado.ioloop.IOLoop.current().add_callback(self.cleanup)

    def has_argument(self, arg_name):
        return arg_name in self.request.query_arguments or arg_name in self.request.body_arguments

    def get_request_uri(self):
        return self.request.path + (("?" + self.request.query) if self.request.query else "")

    async def has_membership(self, role):
        return await auth.has_membership(self, role)
