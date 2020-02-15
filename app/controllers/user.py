from cms4py import http


async def ajax_info(req: http.Request, res: http.Response):
    await res.render("user/ajax_info.html", current_user=None)
