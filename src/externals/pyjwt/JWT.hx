package externals.pyjwt;

import python.Dict;

@:pythonImport("jwt")
extern class JWT {
	public static function encode(data:Dict<String, Dynamic>, secret:String, algorithms:String):String;

	public static function decode(data:String, secret:String, algorithms:String):Dict<String, Dynamic>;
}
