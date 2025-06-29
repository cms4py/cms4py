package top.yunp.cms4py.framework.db.pydal;

@:pythonImport("pydal", "Field")
extern class Field {
	public function new(fieldname:String, ?type:String);

	public function _insert():String;
}
