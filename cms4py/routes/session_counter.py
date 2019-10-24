from ..commons.request_context import RequestContext


class SessionCounter(RequestContext):
    def get(self):
        count = self.get_session("count", 0)
        count += 1
        self.set_session("count", count)
        self.write(f"{count}")
