def sync_with(target, callback):
    with target as it:
        return callback(it)


async def async_with(target, callback):
    async with target as it:
        return await callback(it)
