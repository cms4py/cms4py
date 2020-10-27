from asgiref.wsgi import WsgiToAsgi


class WsgiAction:

    def __init__(self, wsgi_app) -> None:
        super().__init__()
        self._wsgi_to_asgi_app = WsgiToAsgi(wsgi_app)

    async def __call__(self, req, res):
        await self._wsgi_to_asgi_app(req.scope, req.receive, res.send)
        res._body_sent = True
