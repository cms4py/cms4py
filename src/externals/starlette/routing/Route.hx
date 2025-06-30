package externals.starlette.routing;

@:pythonImport("starlette.routing", "Route")
extern class Route extends BaseRoute {
    public function new(re:String, handler:Dynamic);
}