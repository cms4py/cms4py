from ..commons.Cms4pyRequestHandler import Cms4pyRequestHandler


class Register(Cms4pyRequestHandler):

    def get(self):

        self.render("user/register.twig")
