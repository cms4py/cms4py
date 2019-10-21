import tornado.ioloop
import tornado.locale
from tornado.web import HTTPServer

import config
from cms4py import cms4py_app
from cms4py.log import log
from cms4py.db import DbConnector


async def async_init():
    await DbConnector.get_instance().async_init()


if __name__ == "__main__":
    current = tornado.ioloop.IOLoop.current()
    current.add_callback(async_init)

    log.info(f"Server port is {config.PORT}")
    tornado.locale.load_translations(config.TRANSLATIONS_FOLDER)
    server = HTTPServer(cms4py_app)
    server.listen(config.PORT)
    current.start()
