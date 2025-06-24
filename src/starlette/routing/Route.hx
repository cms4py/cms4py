package starlette.routing;
import starlette.requests.Request;
import starlette.responses.Response;

@:pythonImport("starlette.routing", "Route")
extern class Route extends BaseRoute {
    public function new(re:String, handler:(request:Request) -> Response);
}