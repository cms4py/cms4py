from jinja2 import FileSystemLoader, Environment

import config
import asyncio


class TemplateEngine:
    __instance = None

    @staticmethod
    def get_instance():
        if not TemplateEngine.__instance:
            TemplateEngine.__instance = TemplateEngine()
        return TemplateEngine.__instance

    def __init__(self) -> None:
        super().__init__()
        self._jinja2_env = Environment(loader=FileSystemLoader(config.VIEWS_ROOT))

    async def render(self, view, **kwargs) -> bytes:
        return (await self.render_string(view, **kwargs)).encode(config.GLOBAL_CHARSET)

    async def render_string(self, view, **kwargs) -> str:
        rloop = asyncio.get_running_loop()
        tpl = await rloop.run_in_executor(None, self._jinja2_env.get_template, view)
        return await rloop.run_in_executor(None, tpl.render, kwargs)
