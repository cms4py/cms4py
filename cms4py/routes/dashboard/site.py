import sys
from cms4py.commons.request_context import RequestContext
import tornado
from cms4py.commons import auth


class Versions(RequestContext):
    @auth.require_membership("admin")
    async def get(self):
        self.response.title = self.locale.translate("Versions")
        await self.render("dashboard/site/versions.html", tornado_version=tornado.version, python_version=sys.version)
