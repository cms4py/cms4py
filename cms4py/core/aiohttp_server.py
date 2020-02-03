import config
from cms4py.core.handlers import Cms4pyRequestHandler
from .servers import Cms4pyAbstractServer
from aiohttp import web


class AioHttpServer(Cms4pyAbstractServer):

    def __init__(self) -> None:
        super().__init__()
        self._app = web.Application()

    def add_get_route(self, route, handler: Cms4pyRequestHandler) -> "AioHttpServer":
        super().add_get_route(route, handler)

        async def route_handler(request):
            return web.Response(text="Hello World")

        self._app.add_routes([web.get(route, route_handler)])
        return self

    def add_post_route(self, route, handler: Cms4pyRequestHandler) -> "AioHttpServer":
        super().add_post_route(route, handler)
        return self

    def start(self):
        super().start()
        web.run_app(self._app, port=config.PORT)
