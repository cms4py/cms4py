from cms4py.actions.wsgi_action import WsgiAction


def wsgi_app(environ, start_response):
    status = '200 OK'
    output = b'Hello WSGI in WSGI!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]


class app(WsgiAction):

    def __init__(self) -> None:
        super().__init__(wsgi_app)
