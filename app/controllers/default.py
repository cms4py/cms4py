from cms4py import http


async def index(request: http.Request, response: http.Response):
    print(request)
    await response.render("index.html", name="Hello")
