import tornado.ioloop
import tornado.locale
from tornado.web import HTTPServer

import config
from cms4py import cms4py_app
from cms4py.log import log

if __name__ == "__main__":
    log.info(f"Server port is {config.PORT}")
    tornado.locale.load_translations(config.TRANSLATIONS_FOLDER)
    server = HTTPServer(cms4py_app)
    server.listen(config.PORT)
    tornado.ioloop.IOLoop.current().start()
