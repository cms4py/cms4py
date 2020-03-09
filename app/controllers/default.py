from cms4py import http
import config
from cms4py.cache_managers import SessionCacheManager
from cms4py.helpers.url_helper import URL


async def index(request: http.Request, response: http.Response):
    print(request._scope['client'])
    await response.render("index.html")


async def page1(req, res: http.Response):
    await res.redirect(URL('default', 'index'))
