package externals.starlette.responses;

import python.Dict;

@:pythonImport("starlette.responses", "Response")
extern class Response {
    public function new(content:String, ?status_code:Int, ?headers:Dict<String, String>, ?media_type:String);
}