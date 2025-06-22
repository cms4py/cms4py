package top.yunp.cms4py;

import python.Syntax;

class AsgiAppFactory {

	public static function createAsgiApp() {
		Syntax.importFromAs("starlette.applications", "Starlette", "Starlette");
		Syntax.importFromAs("starlette.routing", "Route", "Route");
		Syntax.importFromAs("starlette.responses", "PlainTextResponse", "PlainTextResponse");

		final PTR = Syntax.code("PlainTextResponse");
		final R = Syntax.code("Route");

		final app = Syntax.callNamedUntyped(Syntax.code("Starlette"), {
			routes: [R("/", @async (request) -> PTR("Hello World"))]
		});
		return app;
	}
}
