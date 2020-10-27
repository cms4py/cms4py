


async def counter(req, res):
    count = int((await req.get_session("count")) or '0')
    count += 1
    await req.set_session("count", count)
    await res.end(f"Count: {count}".encode("utf-8"))
