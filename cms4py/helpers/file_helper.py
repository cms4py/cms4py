import asyncio
import os


def read_file(file_path) -> bytes:
    f = open(file_path, "rb")
    file_content = f.read()
    f.close()
    return file_content


async def read_file_async(file_path) -> bytes:
    return await asyncio.get_running_loop().run_in_executor(None, read_file, file_path)


async def file_exists(file_path) -> bool:
    return await asyncio.get_running_loop().run_in_executor(None, os.path.exists, file_path)


async def isfile(file_path) -> bool:
    return await asyncio.get_running_loop().run_in_executor(None, os.path.isfile, file_path)


async def getmtime(file_path):
    return await asyncio.get_running_loop().run_in_executor(None, os.path.getmtime, file_path)
