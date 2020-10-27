

async def hello(req, res):
    words = res.translate("Hello")
    await res.end(words.encode("utf-8"))
