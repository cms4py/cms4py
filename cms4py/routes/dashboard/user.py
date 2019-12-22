from cms4py.commons.request_context import RequestContext
from cms4py.commons import data_grid, auth


class AllUsers(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("All users")
        grid = await data_grid.grid(
            self,
            self.db.auth_user.id > 0,
            order_by=~self.db.auth_user.id,
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
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("All groups")
        grid = await data_grid.grid(
            self,
            self.db.auth_group.id > 0,
            order_by=~self.db.auth_group.id
        )
        await self.render("dashboard/user/all_groups.twig", grid=grid)


class Memberships(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("Memberships")

        grid = await data_grid.grid(
            self,
            (self.db.auth_membership.user_id == self.db.auth_user.id) &
            (self.db.auth_membership.group_id == self.db.auth_group.id) &
            (self.db.auth_user.id > 0),
            order_by=~self.db.auth_membership.id,
            fields=[
                "auth_user.login_name",
                "auth_user.email",
                "auth_group.role",
            ]
        )
        await self.render("dashboard/user/memberships.twig", grid=grid)
