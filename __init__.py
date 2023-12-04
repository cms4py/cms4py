from . import handlers
from . import controllers


async def application(scope, receive, send):
    data_sent = False
    if scope['method'] == 'GET':
        data_sent = await handlers.handle_static_file_request(scope, send)

    if not data_sent:
        data_sent = await handlers.handle_dynamic_request(scope, receive, send)

    if not data_sent:
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [
                [b'content-type', b'text/html'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': b"<h1>Not found</h1>",
        })
    pass
