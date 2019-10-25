from cms4py.commons.request_context import RequestContext
from cms4py.commons import data_grid, auth


class AllUsers(RequestContext):
    @auth.require_membership("admin")
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
        await self.render("dashboard/user/all_users.html", grid=grid)


class AllGroups(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("All groups")
        grid = await data_grid.grid(
            self,
            self.db.user_group.id > 0,
            order_by=~self.db.user_group.id
        )
        await self.render("dashboard/user/all_groups.html", grid=grid)


class Memberships(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("Memberships")

        grid = await data_grid.grid(
            self,
            (self.db.user_membership.user == self.db.user.id) &
            (self.db.user_membership.group == self.db.user_group.id) &
            (self.db.user.id > 0),
            order_by=~self.db.user_membership.id,
            fields=[
                "user.login_name",
                "user.email",
                "user_group.role",
            ]
        )
        await self.render("dashboard/user/memberships.html", grid=grid)
