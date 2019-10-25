from cms4py.commons.request_context import RequestContext
from cms4py.commons import auth


class Index(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        await self.render("dashboard/index.html")
