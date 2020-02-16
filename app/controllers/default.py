from cms4py import http
from cms4py.log_helper import log


async def index(request: http.Request, response: http.Response):
    await response.render("index.html", name="Hello")
