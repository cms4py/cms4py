package externals.aiomysql.connection;

import externals.aiomysql.cursors.Cursor;

@:pythonImport("aiomysql.connection", "Connection")
extern class Connection {
	@async public function cursor(?cursor:Dynamic):Cursor;

	@async public function autocommit(?autocommit:Bool):Bool;

	@async public function begin():Dynamic;

	@async public function commit():Dynamic;

	@async public function rollback():Dynamic;

	@async public function select_db(db:String):Dynamic;

	@async public function show_warnings():Dynamic;

	public function escape(s:String):String;
}
