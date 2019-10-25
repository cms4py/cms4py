import sys
from cms4py.commons.request_context import RequestContext
import tornado


class Versions(RequestContext):
    async def get(self):
        self.response.title = self.locale.translate("Versions")
        await self.render("dashboard/site/versions.twig", tornado_version=tornado.version, python_version=sys.version)
