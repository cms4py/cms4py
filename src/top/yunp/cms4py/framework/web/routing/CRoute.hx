package top.yunp.cms4py.framework.web.routing;
import starlette.routing.Route;

class CRoute {

    public var path(get, null):String;
    public var page(get, null):Page;

    private var _path:String = null;
    private var _page:Page = null;

    public function new(path:String, page:Page) {
        _path = path;
        _page = page;
    }

    private function get_path():String {
        return _path;
    }

    private function get_page():Page {
        return _page;
    }

    @:allow(top.yunp.cms4py.ASGI)
    function toRoute():Route {
        return new Route(path, page.__internal_call__);
    }
}