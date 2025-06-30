package externals.starlette.responses;

@:pythonImport("starlette.responses", "RedirectResponse")
extern class RedirectResponse extends Response {
    public function new(url:String, status_code:Int = 307);
}