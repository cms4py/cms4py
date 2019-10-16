from ..commons.Cms4pyRequestHandler import Cms4pyRequestHandler


class Index(Cms4pyRequestHandler):
    def get(self):
        self.render("index.twig")
