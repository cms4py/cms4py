from ..commons.cms4py_request_context import Cms4pyRequestContext


class SessionCounter(Cms4pyRequestContext):
    def get(self):
        count = self.get_session("count", 0)
        count += 1
        self.set_session("count", count)
        self.write(f"{count}")
