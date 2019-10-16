import tornado.web

import config
from .routes import routes

routes.append(
    (
        r"/{}/(.*)".format(config.STATIC_FILES_URL_PATH),
        tornado.web.StaticFileHandler,
        dict(
            path=config.STATIC_FILES_ROOT,
            default_filename=config.DEFAULT_STATIC_FILE_NAME
        )
    )
)

cms4py_app = tornado.web.Application(routes, cookie_secret=config.COOKIE_SECRET)
