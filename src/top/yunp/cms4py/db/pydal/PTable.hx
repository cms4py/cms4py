package top.yunp.cms4py.db.pydal;

import top.yunp.cms4py.logger.Logger;
import top.yunp.cms4py.lib.FuncTools;

class PTable {
	private var _table:Dynamic = null;
	private var _op:PTableOp;

	public function new(table:Dynamic) {
		_table = table;
		_op = new PTableOp(this);
	}

	public function field(name:String):Dynamic {
		return Reflect.field(_table, name);
	}

	public function f(name:String):Dynamic {
		return field(name);
	}

	public var op(get, null):PTableOp;

	private function get_op():PTableOp {
		return _op;
	}

	@:allow(top.yunp.cms4py.db.pydal.PTable)
	private function get_original_table() {
		return _table;
	}
}

abstract PTableOp(PTable) {
	public inline function new(t:PTable) {
		this = t;
	}

	public function insert(data:Dynamic):String {
		var sql = FuncTools.callNamed(this.get_original_table()._insert, data);
		Logger.debug(sql);
		return sql;
	}

	@:op([])
	@:op(a.b)
	public function field(name:String):Dynamic {
		return this.field(name);
	}
}
