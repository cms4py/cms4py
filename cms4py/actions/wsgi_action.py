from asgiref.wsgi import WsgiToAsgi
from .asgi_action import AsgiAction


class WsgiAction(AsgiAction):

    def __init__(self, wsgi_app) -> None:
        super().__init__(WsgiToAsgi(wsgi_app))
