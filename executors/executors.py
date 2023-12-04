import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

thread_pool_executor = ThreadPoolExecutor()
process_pool_executor = ProcessPoolExecutor()


async def run_in_thread_pool_executor(target):
    return await asyncio.get_running_loop().run_in_executor(
        thread_pool_executor, target
    )


async def run_in_process_pool_executor(target):
    return await asyncio.get_running_loop().run_in_executor(
        process_pool_executor, target
    )
