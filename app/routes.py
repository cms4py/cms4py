from cms4py.core.servers import Cms4pyAbstractServer
from app.pages.index import IndexPage
from cms4py.core.log import log


def config(server: Cms4pyAbstractServer) -> Cms4pyAbstractServer:
    server.add_get_route("/", IndexPage())
    return server
