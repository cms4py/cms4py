package externals.starlette.responses;
import python.Dict;

@:pythonImport("starlette.responses", "HTMLResponse")
extern class HTMLResponse extends Response {
    public function new(content:String, ?status_code:Int, ?headers:Dict<String, String>, ?media_type:String);
}