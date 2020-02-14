from .core.servers import Cms4pyAbstractServer


def create_server(aio_lib='aiohttp') -> Cms4pyAbstractServer:
    """
    :param aio_lib: Can be "aiohttp" or "tornado"
    :return:
    """
    if aio_lib == 'aiohttp':
        from .core.servers.aiohttp_server import AioHttpServer
        server = AioHttpServer()
    elif aio_lib == "tornado":
        from .core.servers.tornado_server import TornadoServer
        server = TornadoServer()
    else:
        raise Exception(f"aio lib '{aio_lib}' is not supported.")
    return server
