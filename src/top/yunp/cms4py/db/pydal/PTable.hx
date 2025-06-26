package top.yunp.cms4py.db.pydal;

import top.yunp.cms4py.logger.Logger;
import top.yunp.cms4py.lib.FuncTools;

abstract PTable(Dynamic) {
	public inline function new(table:Dynamic) {
		this = table;
	}

	@:op([])
	@:op(a.b)
	public function field(name:String):Dynamic {
		return Reflect.field(this, name);
	}

	public function f(name:String):Dynamic {
		return field(name);
	}

	public function insert(data:Dynamic):String {
		var sql = FuncTools.callNamed(this._insert, data);
		Logger.debug(sql);
		return sql;
	}
}
