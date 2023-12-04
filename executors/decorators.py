from cms4py.executors.executors import run_in_thread_pool_executor


def in_thread_pool(target):
    async def inner(*args, **kwargs):
        return await run_in_thread_pool_executor(lambda: target(*args, **kwargs))

    return inner
