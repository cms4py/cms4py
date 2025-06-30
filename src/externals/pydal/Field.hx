package externals.pydal;

@:pythonImport("pydal", "Field")
extern class Field {
	public function new(fieldname:String, ?type:String);

	public function _insert():String;
}
