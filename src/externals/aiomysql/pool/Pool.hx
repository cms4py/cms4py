package externals.aiomysql.pool;

import externals.aiomysql.connection.Connection;

@:pythonImport("aiomysql.pool", "Pool")
extern class Pool {
	@async public function acquire():Connection;

	@async public function release(conn:Connection):Dynamic;
}
