class AsgiAction:
    def __init__(self, asgi_app) -> None:
        super().__init__()
        self._asgi_app = asgi_app

    async def __call__(self, req, res):
        await self._asgi_app(req.scope, req.receive, res.send)
        res._body_sent = True
