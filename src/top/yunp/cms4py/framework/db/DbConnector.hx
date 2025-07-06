package top.yunp.cms4py.framework.db;

import haxe.Exception;
import python.Syntax;
import top.yunp.cms4py.framework.db.Aiomysql;
import externals.aiomysql.cursors.DictCursor;
import top.yunp.cms4py.framework.db.PCursor;
import externals.aiomysql.pool.Pool;
import top.yunp.cms4py.framework.lib.Traceback;
import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.web.Server;

@:build(hxasync.AsyncMacro.build())
class DbConnector {
	private static var _instance:DbConnector = null;

	public static function getInstance():DbConnector {
		if (_instance == null) {
			_instance = new DbConnector();
		}
		return _instance;
	}

	private var _pool:Pool = null;

	public function new() {}

	@:allow(top.yunp.cms4py.ASGI)
	@async private function createPool() {
		_pool = @await Syntax.callNamedUntyped(Aiomysql.create_pool, {
			host: Server.web.dbHost,
			port: Server.web.dbPort,
			user: Server.web.dbUser,
			password: Server.web.dbPassword,
			db: Server.web.dbName,
			minsize: Server.web.dbPoolMinsize,
			maxsize: Server.web.dbPoolMaxsize,
		});
		return _pool;
	}

	@async public function use(handler:(cursor:PCursor) -> Dynamic):Dynamic {
		var conn = @await _pool.acquire();
		@await conn.autocommit(false);
		var cursor = new PCursor(@await conn.cursor(DictCursor));
		var result:Dynamic = null;
		try {
			result = @await handler(cursor);
		} catch (e:Exception) {
			@await conn.rollback();
			Logger.info(e);
			Traceback.print_exc();
		}
		if (cursor.modified) {
			@await conn.commit();
		}
		@await cursor.close();
		@await _pool.release(conn);
		return result;
	}
}
