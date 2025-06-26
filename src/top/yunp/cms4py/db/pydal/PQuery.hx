package top.yunp.cms4py.db.pydal;

import top.yunp.cms4py.logger.Logger;
import top.yunp.cms4py.lib.FuncTools;

class PQuery {
	private var _dalQuery:Dynamic;

	public function new(dalQuery) {
		_dalQuery = dalQuery;
	}

	public function select(?fields:Array<Dynamic>, ?options:Dynamic):String {
		var sql = FuncTools.call(_dalQuery._select, fields, options);
		Logger.debug(sql);
		return sql;
	}

	public function count() {
		var sql = _dalQuery._count();
		Logger.debug(sql);
		return sql;
	}
}
