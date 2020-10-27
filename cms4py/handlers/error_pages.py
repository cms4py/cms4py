

async def send_404_error(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 404,
        'headers': [
            [b'content-type', b'text/html'],
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': b"Not found",
        'more_body': False
    })
