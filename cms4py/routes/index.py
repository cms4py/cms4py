from ..commons.request_context import RequestContext


class Index(RequestContext):
    def get(self):
        self.render("index.twig")
