from cms4py.core.handlers import Cms4pyRequestHandler, Cms4pyRequestHandlerContext


class IndexPage(Cms4pyRequestHandler):

    async def pre_execute(self, context: "Cms4pyRequestHandlerContext"):
        return await super().pre_execute(context)

    async def execute(self, context: "Cms4pyRequestHandlerContext"):
        context.response.append("Hello World1")

    async def post_execute(self, context: "Cms4pyRequestHandlerContext"):
        return await super().post_execute(context)
