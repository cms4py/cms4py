package top.yunp.cms4py;

import python.Dict;
import python.Syntax;
import Routes;
import top.yunp.cms4py.logger.Logger;
import top.yunp.cms4py.db.DbConnector;

@:build(hxasync.AsyncMacro.build())
class ASGI {
    private static function createStarletteAsgiApp() {
        Syntax.importFromAs("starlette.applications", "Starlette", "Starlette");

        final app = Syntax.callNamedUntyped(Syntax.code("Starlette"), {
            routes: Routes.createRoutes()
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
                    var r = new Dict<String, String>();
                    r.set("type", "lifespan.startup.complete");
                    @await send(r);
                    break;
                case "lifespan.shutdown":
                    if (pool != null) {
                        pool.close();
                        @await pool.wait_closed();
                    }
                    var r = new Dict<String, String>();
                    r.set("type", "lifespan.shutdown.complete");
                    @await send(r);
                    break;
                default :
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
