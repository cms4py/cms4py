import config
from cms4py.core.handlers import Cms4pyRequestHandler, Cms4pyRequestHandlerContext
from cms4py.core.servers import Cms4pyAbstractServer
from aiohttp import web
from cms4py.core.http import Request, Response


class AioHttpServer(Cms4pyAbstractServer):

    def __init__(self) -> None:
        super().__init__()
        self._app = web.Application()

    def add_route(self, route, func, handler: Cms4pyRequestHandler) -> "AioHttpServer":
        async def route_handler(request):
            context = Cms4pyRequestHandlerContext()
            context.request = Request(request)
            context.response = Response()
            await handler.pre_execute(context)
            await handler.execute(context)
            result = web.Response(text=context.response.data)
            await handler.post_execute(context)
            return result

        self._app.add_routes([func(route, route_handler)])
        return self

    def add_get_route(self, route, handler: Cms4pyRequestHandler) -> "AioHttpServer":
        super().add_get_route(route, handler)
        self.add_route(route, web.get, handler)
        return self

    def add_post_route(self, route, handler: Cms4pyRequestHandler) -> "AioHttpServer":
        super().add_post_route(route, handler)
        self.add_route(route, web.post, handler)
        return self

    def start(self):
        super().start()
        web.run_app(self._app, port=config.PORT)
