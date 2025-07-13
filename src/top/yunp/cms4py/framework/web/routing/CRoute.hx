package top.yunp.cms4py.framework.web.routing;

import top.yunp.cms4py.framework.lib.FuncTools;
import externals.starlette.routing.Route;

class CRoute {
	public var path(get, null):String;
	public var page(get, null):Page;

	private var _path:String = null;
	private var _page:Page = null;
	private var _methods:Array<String> = null;

	public function new(path:String, page:Page, ?methods:Array<String>) {
		_path = path;
		_page = page;
		_methods = methods;
	}

	private function get_path():String {
		return _path;
	}

	private function get_page():Page {
		return _page;
	}

	@:allow(top.yunp.cms4py.ASGI)
	function toRoute():Route {
		var args:Dynamic = {path: path, endpoint: page.__internal_call__};
		if (_methods != null) {
			args.methods = _methods;
		}
		return FuncTools.callNamed(Route, args);
	}
}
