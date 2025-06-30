package externals.starlette.requests;

import python.Dict;

@:pythonImport("starlette.requests", "Request")
extern class Request {
	public final path_params:Dict<String, String>;
}
