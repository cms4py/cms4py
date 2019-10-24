from ..commons.cms4py_request_context import Cms4pyRequestContext


class Index(Cms4pyRequestContext):
    def get(self):
        self.render("index.twig")
