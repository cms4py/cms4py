from ..commons.cms4py_request_context import Cms4pyRequestContext
from ..commons.url import URL
from ..commons import auth


class Register(Cms4pyRequestContext):

    async def get(self):
        await self.render(
            "user/register.twig",
            login_name="", email="", phone="", password="",
            nickname=""
        )

    async def post(self):
        db = self.db
        login_name = self.get_argument("login_name")
        email = self.get_argument("email")
        phone = self.get_argument("phone")
        password = self.get_argument("password")
        password = db.user.password.requires(password)[0]
        nickname = self.get_argument("nickname")

        if (await self.db.user.insert(
                login_name=login_name, email=email, phone=phone, password=password,
                nickname=nickname
        )):
            user_record = (await db(db.user.login_name == login_name).select()).first()
            self.set_current_user(user_record)
            self.redirect(URL("user", "profile"))
        else:
            self.response.alert = self.locale.translate("Failed to register")
            await self.render(
                "user/register.twig"
            )


class Login(Cms4pyRequestContext):
    async def get(self):
        self.response.title = self.locale.translate("Login")
        await self.render("user/login.twig")

    async def post(self):
        login_param = self.get_argument("login")
        password = self.get_argument("password")
        db = self.db
        user_record = (await db(
            (db.user.login_name == login_param) |
            (db.user.email == login_param) |
            (db.user.phone == login_param)
        ).select()).first()
        if user_record:
            transcode = db.user.password.requires(password)[0]
            if transcode == user_record.password:
                self.set_current_user(user_record)
                _next = self.get_query_argument("_next", None)
                if _next:
                    self.redirect(_next)
                    return
                else:
                    self.redirect(URL("user", "profile"))
                    return
        self.response.alert = self.locale.translate("Invalid login, login name or password wrong!")
        await self.render("user/login.twig")


class Profile(Cms4pyRequestContext):

    @auth.require_login
    async def get(self):
        await self.render("user/profile.twig")


class Logout(Cms4pyRequestContext):

    async def get(self):
        self.set_current_user(None)
        _next = self.get_argument("_next", None)
        if _next:
            self.redirect(_next)
        else:
            self.redirect("/")


class AjaxInfo(Cms4pyRequestContext):

    async def get(self):
        await self.render("user/ajax_info.twig")
