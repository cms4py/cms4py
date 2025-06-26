package top.yunp.cms4py.db.aiomysql.cursors;

import top.yunp.cms4py.db.pydal.PTable;
import python.Dict;
import top.yunp.cms4py.db.pydal.PDAL;

@:build(hxasync.AsyncMacro.build())
class PCursor {
	private var _cursor:Cursor = null;
	private var _modified = false;

	public function new(cursor:Cursor) {
		_cursor = cursor;
	}

	@async public function close() {
		@await _cursor.close();
	}

	@async public function execute(query:String, ?args:Dynamic):Dynamic {
		_modified = true;
		return @await _cursor.execute(query, args);
	}

	@async public function fetchall():Dynamic {
		return @await _cursor.fetchall();
	}

	@async public function count(query:Dynamic) {
		var db = PDAL.getInstance().op;
		var rows = @await _cursor.execute(db(query).count());
		if (rows != 1) {
			return 0;
		}
		var resultSet = @await fetchall();
		var first:Dict<String, Dynamic> = resultSet[0];
		return first.iterator().next();
	}

	@async public function select(query:Dynamic, ?fields:Array<Dynamic>, ?options:Dynamic):Array<Dict<String, Dynamic>> {
		var db = PDAL.getInstance().op;
		@await _cursor.execute(db(query).select(fields, options));
		return @await fetchall();
	}

	public var modified(get, null):Bool;

	private function get_modified():Bool {
		return _modified;
	}

	@async public function insert(table:PTableOp, data:Dynamic):Dynamic {
		return @await execute(table.insert(data));
	}
}
