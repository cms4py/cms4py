from cms4py.commons.request_context import RequestContext
from cms4py.commons import data_grid


class AllUsers(RequestContext):
    async def get(self):
        self.response.title = self.locale.translate("All users")
        grid = await data_grid.grid(
            self,
            self.db.user.id > 0,
            order_by=~self.db.user.id,
            fields=[
                "id",
                "login_name",
                "nickname",
                "email",
                "phone"
            ]
        )
        await self.render("dashboard/user/all_users.twig", grid=grid)


class AllGroups(RequestContext):
    async def get(self):
        self.response.title = self.locale.translate("All groups")
        grid = await data_grid.grid(
            self,
            self.db.user_group.id > 0,
            order_by=~self.db.user_group.id
        )
        await self.render("dashboard/user/all_groups.twig", grid=grid)
