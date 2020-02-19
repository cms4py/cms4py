from cms4py import http
import config
from cms4py.cache_managers import SessionCacheManager
from cms4py.helpers.url_helper import URL


async def index(request: http.Request, response: http.Response):
    print(SessionCacheManager.get_instance().cache_map)
    await request.set_session("count", (await request.get_session("count", 0)) + 1)
    await response.render("index.html", name="Hello", count=await request.get_session("count"))


async def page1(req, res: http.Response):
    await res.redirect(URL('default', 'index'))
