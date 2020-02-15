from cms4py import http


async def index(request: http.Request, response: http.Response):
    await response.write(b"Hello World")
