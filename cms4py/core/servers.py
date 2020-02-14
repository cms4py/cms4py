from cms4py.core.servers import Cms4pyRequestHandler


class Cms4pyAbstractServer:
    def add_get_route(self, route, handler: Cms4pyRequestHandler):
        pass

    def add_post_route(self, route, handler: Cms4pyRequestHandler):
        pass

    def start(self):
        pass
