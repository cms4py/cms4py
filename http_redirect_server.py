import asyncio
import sys
from threading import Thread

import tornado.ioloop
import tornado.platform.asyncio
import tornado.web

import config
from cms4py.helpers.log_helper import Cms4pyLog


class RedirectToHttpsHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(f"https://{self.request.host_name}{self.request.uri}", True)


class HttpServer(Thread):
    """
    Every access to this server will be redirect to the https server
    """
    __current_instance = None

    @staticmethod
    def current_instance():
        if not HttpServer.__current_instance:
            HttpServer.__current_instance = HttpServer()
        return HttpServer.__current_instance

    def stop(self):
        self._stopped = True

    async def check_if_stopped(self):
        while True:
            await asyncio.sleep(2)
            if self._stopped:
                tornado.ioloop.IOLoop.current().stop()
                break

    async def listen_if_stopped(self):
        self._stopped = False
        asyncio.create_task(self.check_if_stopped())

    def run(self) -> None:
        asyncio.set_event_loop_policy(tornado.platform.asyncio.AnyThreadEventLoopPolicy())
        print(f"Http server started at port {config.HTTP_PORT}", file=sys.stderr)
        tornado.web.Application([
            (r".*", RedirectToHttpsHandler)
        ]).listen(config.HTTP_PORT)
        current = tornado.ioloop.IOLoop.current()
        current.add_callback(self.listen_if_stopped)
        current.start()
        super().run()
        HttpServer.__current_instance = None
        Cms4pyLog.get_instance().info("Http redirect server is stopped")
