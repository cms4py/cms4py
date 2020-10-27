
async def counter(req, res):
    count = int(req.get_cookie(b"count") or b'0')
    count += 1
    res.add_set_cookie(b'count', str(count).encode("utf-8"))
    await res.end(f"Count: {count}".encode("utf-8"))
