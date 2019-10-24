from .cms4py_request_context import Cms4pyRequestContext
from .url import URL


def require_login(func):
    async def wrapper(self: Cms4pyRequestContext):
        if self.current_user:
            await func(self)
        else:
            self.redirect(URL("user", "login", vars=dict(_next=self.get_request_uri())))

    return wrapper
