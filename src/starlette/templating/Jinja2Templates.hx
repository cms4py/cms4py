package starlette.templating;
import starlette.responses.HTMLResponse;
import python.Dict;
import starlette.requests.Request;

@:pythonImport("starlette.templating", "Jinja2Templates")
extern class Jinja2Templates {
    public function new(directory:String);

    public function TemplateResponse(request:Request, name:String, ?context:Dict<String, Any>, ?status_code:Int, ?headers:Dict<String, String>, ?media_type:String):HTMLResponse;
}