from cms4py.core.handlers import Cms4pyRequestHandler
from cms4py.core.servers import Cms4pyAbstractServer


class TornadoServer(Cms4pyAbstractServer):
    def add_get_route(self, route, handler: Cms4pyRequestHandler):
        super().add_get_route(route, handler)

    def add_post_route(self, route, handler: Cms4pyRequestHandler):
        super().add_post_route(route, handler)
