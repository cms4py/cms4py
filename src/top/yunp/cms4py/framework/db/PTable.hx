package top.yunp.cms4py.framework.db;

import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.lib.FuncTools;

abstract PTable(Dynamic) {
	public inline function new(table:Dynamic) {
		this = table;
	}

	@:op([])
	@:op(a.b)
	public function field(name:String):Dynamic {
		var f = Reflect.field(this, name);
		return f;
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
