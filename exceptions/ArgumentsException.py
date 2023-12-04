"""
Created on 2023/12/04
"""
from cms4py.exceptions.Cms4pyException import Cms4pyException


class ArgumentsException(Cms4pyException):
    def __init__(self):
        super().__init__("Arguments Exception")
