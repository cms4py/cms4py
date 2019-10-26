from cms4py.commons.request_context import RequestContext
from cms4py.commons import data_grid, auth


class AllUsers(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("All users")
        grid = await data_grid.grid(
            self,
            self.db.member.id > 0,
            order_by=~self.db.member.id,
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
            self.db.member_group.id > 0,
            order_by=~self.db.member_group.id
        )
        await self.render("dashboard/user/all_groups.twig", grid=grid)


class Memberships(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("Memberships")

        grid = await data_grid.grid(
            self,
            (self.db.membership.user_id == self.db.member.id) &
            (self.db.membership.group_id == self.db.member_group.id) &
            (self.db.member.id > 0),
            order_by=~self.db.membership.id,
            fields=[
                "member.login_name",
                "member.email",
                "member_group.role",
            ]
        )
        await self.render("dashboard/user/memberships.twig", grid=grid)
