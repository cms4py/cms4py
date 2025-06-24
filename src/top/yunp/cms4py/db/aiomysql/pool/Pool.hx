package top.yunp.cms4py.db.aiomysql.pool;

import top.yunp.cms4py.db.aiomysql.connection.Connection;

@:pythonImport("aiomysql.pool", "Pool")
extern class Pool {
	@async public function acquire():Connection;

	@async public function release(conn:Connection):Dynamic;
}
