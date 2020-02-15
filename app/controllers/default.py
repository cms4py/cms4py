from cms4py import http


async def index(request: http.Request, response: http.Response):
    await response.render("index.html")
