import tornado.web

import config
from .routes import routes
from cms4py.socketio import socketio_tornado_handler

routes.append(
    (r"/socket.io/", socketio_tornado_handler)
)

routes.append(
    (
        r"/(.*)",
        tornado.web.StaticFileHandler,
        dict(
            path=config.STATIC_FILES_ROOT,
            default_filename=config.DEFAULT_STATIC_FILE_NAME
        )
    )
)

cms4py_app = tornado.web.Application(routes, cookie_secret=config.COOKIE_SECRET)
