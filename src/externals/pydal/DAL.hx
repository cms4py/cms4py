package externals.pydal;

import haxe.Rest;

@:pythonImport("pydal", "DAL")
extern class DAL {
	public function new(connect_string:String);

	public function define_table(tablename:String, fields:Rest<Field>):Dynamic;
}
