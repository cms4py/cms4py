from ..commons.Cms4pyRequestContext import Cms4pyRequestContext


class Index(Cms4pyRequestContext):
    def get(self):
        self.render("index.twig")
