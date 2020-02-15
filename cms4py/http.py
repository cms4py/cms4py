class Request:
    def __init__(self, scope, receive):
        self._scope = scope
        self._receive = receive
        pass
    pass


class Response:
    def __init__(self, send):
        self._send = send
        pass
    pass
