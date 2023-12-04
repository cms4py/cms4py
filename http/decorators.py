"""
Created on 2023/12/04
@author: topyunp.com
"""

from cms4py.exceptions.ArgumentsException import ArgumentsException
from cms4py.exceptions.HttpException import HttpException
from cms4py.http import Request


def allow_get_method_only(f):
    async def inner(*args):
        arg_len = len(args)
        if arg_len == 2:
            req: Request = args[0]
        elif arg_len == 3:
            req: Request = args[1]
        else:
            raise ArgumentsException()
        if req.method != "GET":
            raise HttpException(405, b"Method Not Allowed")
        return await f(*args)

    return inner
