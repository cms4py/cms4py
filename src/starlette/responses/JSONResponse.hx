package starlette.responses;

@:pythonImport("starlette.responses", "JSONResponse")
extern class JSONResponse extends Response {
    public function new(content:String);
}