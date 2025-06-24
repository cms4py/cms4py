package top.yunp.cms4py.db;

import python.Syntax;
import top.yunp.cms4py.web.Server;
import top.yunp.cms4py.logger.Logger;
import top.yunp.cms4py.lib.AsyncIO;
import top.yunp.cms4py.db.aiomysql.Aiomysql;
import top.yunp.cms4py.db.aiomysql.connection.Connection;
import haxe.Exception;
import top.yunp.cms4py.lib.Traceback;
import top.yunp.cms4py.db.aiomysql.cursors.Cursor;

@:build(hxasync.AsyncMacro.build())
class DbConnector {

    private static var _instance:DbConnector = null;

    public static function getInstance():DbConnector {
        if (_instance == null) {
            _instance = new DbConnector();
        }
        return _instance;
    }

    private var _pool:Dynamic = null;

    public function new() {
    }

    @:allow(top.yunp.cms4py.ASGI)
    @async private function createPool() {
        _pool = @await Syntax.callNamedUntyped(Aiomysql.create_pool, {
            host:Server.web.get("dbHost"),
            port:Server.web.get("dbPort"),
            user:Server.web.get("dbUser"),
            password:Server.web.get("dbPassword"),
            db:Server.web.get("dbName"),
            minsize:Server.web.get("dbPoolMinsize"),
            maxsize:Server.web.get("dbPoolMaxsize"),
        });
        return _pool;
    }

    @async public function use(@async handler:(cursor:Cursor) -> Dynamic) {
        var conn:Connection = @await _pool.acquire();
        var cursor = @await conn.cursor();
        try {
            @await handler(cursor);
        } catch (e:Exception) {
            Logger.info(e);
            Traceback.print_exc();
        }
        @await cursor.close();
        @await _pool.release(conn);
    }
}