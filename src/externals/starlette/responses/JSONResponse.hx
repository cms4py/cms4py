package externals.starlette.responses;

import python.Dict;

@:pythonImport("starlette.responses", "JSONResponse")
extern class JSONResponse extends Response {
	public function new(content:Dict<Dynamic, Dynamic>);
}
