from cms4py import http


async def index(request: http.Request, response: http.Response):
    await response._send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
                [b'content-type', b'text/html'],
        ]
    })
    await response._send({
        'type': 'http.response.body',
        'body': b"Hello World",
    })
    pass
