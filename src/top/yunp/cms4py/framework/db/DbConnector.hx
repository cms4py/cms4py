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
import externals.py.lang.PyWith;

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
		var r0 = @await PyWith.async_with(_pool.acquire(), @async conn -> {
			@await conn.autocommit(false);
			var r1 = @await PyWith.async_with(conn.cursor(DictCursor), @async cur -> {
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
				return result;
			});
			return r1;
		});
		return r0;
	}
}
