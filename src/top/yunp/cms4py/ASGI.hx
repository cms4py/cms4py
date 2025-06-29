package top.yunp.cms4py;

import Routes;
import python.Syntax;
import python.lib.os.Path;
import starlette.applications.Starlette;
import starlette.routing.Mount;
import starlette.staticfiles.StaticFiles;
import top.yunp.cms4py.framework.db.DbConnector;
import top.yunp.cms4py.framework.lib.FuncTools;
import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.utils.ObjectUtils;
import top.yunp.cms4py.framework.web.Server;
import top.yunp.cms4py.framework.web.routing.CRoute;

@:build(hxasync.AsyncMacro.build())
class ASGI {
	private static function createStarletteAsgiApp() {
		var routes:Array<CRoute> = Routes.configRoutes();

		var r:Array<Dynamic> = routes.map(c -> c.toRoute());
		r.push(FuncTools.callNamed(Mount, {
			path: "/static",
			app: FuncTools.callNamed(StaticFiles, {
				directory: Path.join(Server.projectRoot, Server.web.get("staticRoot")),
				html: true
			})
		}));

		final app = FuncTools.callNamed(Starlette, {
			routes: r
		});
		return app;
	}

	@async public static function lifespanHandler(scope:Dynamic, receive:Dynamic, send:Dynamic) {
		while (true) {
			var message = @await receive();
			var pool:Dynamic = null;
			switch (Syntax.arrayAccess(message, "type")) {
				case "lifespan.startup":
					pool = @await DbConnector.getInstance().createPool();
					@await send(ObjectUtils.toDict({type: "lifespan.startup.complete"}));
					break;
				case "lifespan.shutdown":
					if (pool != null) {
						pool.close();
						@await pool.wait_closed();
					}
					@await send(ObjectUtils.toDict({type: "lifespan.shutdown.complete"}));
					break;
				default:
					Logger.warn('Unsupported message type ${Syntax.arrayAccess(message, "type")}');
			}
		}
	}

	private static var _starletteApp:Dynamic = null;

	@async public static function app(scope:Dynamic, receive:Dynamic, send:Dynamic) {
		if (_starletteApp == null) {
			_starletteApp = createStarletteAsgiApp();
		}

		if (Syntax.arrayAccess(scope, "type") == "lifespan") {
			return @await lifespanHandler(scope, receive, send);
			return;
		}

		return @await _starletteApp(scope, receive, send);
	}
}
