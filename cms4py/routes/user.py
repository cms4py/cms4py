from ..commons import Cms4pyRequestContext


class Register(Cms4pyRequestContext.Cms4pyRequestContext):

    def get(self):
        self.render(
            "user/register.twig",
            login_name="", email="", phone="", password="",
            nickname=""
        )

    def post(self):
        login_name = self.get_argument("login_name")
        email = self.get_argument("email")
        phone = self.get_argument("phone")
        password = self.get_argument("password")
        nickname = self.get_argument("nickname")
        self.db.user.insert(login_name=login_name, email=email, phone=phone, password=password, nickname=nickname)
        self.render(
            "user/register.twig", login_name=login_name, email=email, phone=phone, password=password,
            nickname=nickname
        )