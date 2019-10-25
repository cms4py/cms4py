from ..commons.request_context import RequestContext


class Index(RequestContext):

    async def get(self):
        await self.render("index.twig")
