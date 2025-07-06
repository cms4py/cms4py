/*
 * MIT License
 *
 * Copyright (c) 2025 https://yunp.top
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
 * Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
 * AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
 * THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
 
package top.yunp.cms4py;

import Routes;
import python.Syntax;
import python.Lib;
import python.lib.os.Path;
import externals.starlette.applications.Starlette;
import externals.starlette.routing.Mount;
import externals.starlette.staticfiles.StaticFiles;
import top.yunp.cms4py.framework.db.DbConnector;
import top.yunp.cms4py.framework.lib.FuncTools;
import top.yunp.cms4py.framework.logger.Logger;
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
				directory: Path.join(Server.projectRoot, Server.web.staticRoot),
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
					@await send(Lib.anonAsDict({type: "lifespan.startup.complete"}));
					break;
				case "lifespan.shutdown":
					if (pool != null) {
						pool.close();
						@await pool.wait_closed();
					}
					@await send(Lib.anonAsDict({type: "lifespan.shutdown.complete"}));
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
