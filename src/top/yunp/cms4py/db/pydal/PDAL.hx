package top.yunp.cms4py.db.pydal;

import python.Syntax;
import top.yunp.cms4py.web.Server;
import top.yunp.cms4py.db.pydal.PTable.PTableOp;

class PDAL {
	private static var _instance:PDAL = null;

	public static function getInstance():PDAL {
		if (_instance == null) {
			_instance = new PDAL();
		}
		return _instance;
	}

	private var _dal:DAL;
	private var _pdalOp:PDALOp;

	public function new() {
		var web = Server.web;
		var uri = '${web.get("db")}://${web.get("dbUser")}:${web.get("dbPassword")}@${web.get("dbHost")}:${web.get("dbPort")}/${web.get("dbName")}';
		_dal = Syntax.callNamedUntyped(DAL, {
			uri: uri,
			migrate: false,
			migrate_enabled: false,
			bigint_id: true
		});
		Tables.defineTables(_dal);

		_pdalOp = new PDALOp(this);
	}

	private var _tables:Map<String, PTableOp> = new Map();

	public function table(name:String):PTableOp {
		if (_tables.exists(name)) {
			return _tables.get(name);
		} else {
			var t = new PTable(Reflect.field(_dal, name)).op;
			_tables.set(name, t);
			return t;
		}
	}

	public function t(name:String):PTableOp {
		return table(name);
	}

	public function query(?_query:Dynamic):PQuery {
		var d:Dynamic = _dal;
		return new PQuery(d(_query));
	}

	public function q(?_q:Dynamic):PQuery {
		return query(_q);
	}

	public var op(get, null):PDALOp;

	private function get_op():PDALOp {
		return _pdalOp;
	}
}

abstract PDALOp(PDAL) {
	public inline function new(dal:PDAL) {
		this = dal;
	}

	@:op([])
	@:op(a.b)
	public function table(name:String):PTableOp {
		return this.table(name);
	}

	@:op(a())
	public function query(q:Dynamic):PQuery {
		return this.query(q);
	}
}
