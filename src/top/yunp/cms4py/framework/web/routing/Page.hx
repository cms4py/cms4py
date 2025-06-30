package top.yunp.cms4py.framework.web.routing;

import haxe.exceptions.NotImplementedException;
import externals.starlette.requests.Request;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.db.DbConnector;
import top.yunp.cms4py.framework.db.PCursor;
import top.yunp.cms4py.framework.db.pydal.PDAL;
import top.yunp.cms4py.framework.web.templating.Templates;

@:build(hxasync.AsyncMacro.build())
class Page {
	public var db(get, null):PDALOp;

	private function get_db():PDALOp {
		return PDAL.getInstance().op;
	}

	@async public function execute(request:Request):Response {
		throw new NotImplementedException();
	}

	public function templateResponse(request:Request, name:String, ?context:Dynamic):Response {
		return Templates.getInstance().response(request, name, context);
	}

	@async public function useCursor(handler:(cursor:PCursor) -> Dynamic):Dynamic {
		return @await DbConnector.getInstance().use(handler);
	}

	@:allow(top.yunp.cms4py.framework.web.routing.CRoute)
	@async function __internal_call__(request:Request):Response {
		var req:Dynamic = request;
		req.siteName = Server.web.get("siteName");
		return @await execute(req);
	}
}
