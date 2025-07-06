package externals.py.lang;

@:pythonImport("py.lang", "PyWith")
extern class PyWith {
	public static function sync_with(target:Dynamic, callback:(it:Dynamic) -> Dynamic):Dynamic;
	@async public static function async_with(target:Dynamic, callback:(it:Dynamic) -> Dynamic):Dynamic;
}
