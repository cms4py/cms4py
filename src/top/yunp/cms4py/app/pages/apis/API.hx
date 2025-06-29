package top.yunp.cms4py.app.pages.apis;

import python.Dict;
import python.lib.Json;
import starlette.requests.Request;
import starlette.responses.JSONResponse;
import starlette.responses.Response;
import top.yunp.cms4py.app.pages.apis.actions.Action;
import top.yunp.cms4py.app.pages.apis.actions.Actions;
import top.yunp.cms4py.framework.web.routing.Page;

@:build(hxasync.AsyncMacro.build())
class API extends Page {
	public function new() {}

	private var _actions = new Map<String, Action>();

	public function addAction(name:String, action:Action) {
		_actions.set(name, action);
	}

	public var actions(get, never):Map<String, Action>;

	private function get_actions():Map<String, Action> {
		return _actions;
	}

	@async override function execute(request:Request):Response {
		var actionName = request.path_params.get("action");
		var result:Dict<String, Dynamic> = null;
		if (actions.exists(actionName)) {
			result = @await actions.get(actionName).doAction(request);
		} else {
			result = Actions.createResult(Actions.CODE_ACTION_NOT_FOUND, "Action not found");
		}
		return new JSONResponse(Json.dumps(result));
	}
}
