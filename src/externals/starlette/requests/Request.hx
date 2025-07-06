package externals.starlette.requests;

import python.Dict;

@:pythonImport("starlette.requests", "Request")
extern class Request {
	public final method:String;
	public final url:Dynamic;
	public final client:Dynamic;
	public final path_params:Dict<String, String>;
	public final query_params:Dict<String, String>;
	public final headers:Dict<String, String>;
	public final cookies:Dict<String, String>;

	@async public function body():Dynamic;
	@async public function form():Dynamic;
	@async public function json():Dynamic;
}
