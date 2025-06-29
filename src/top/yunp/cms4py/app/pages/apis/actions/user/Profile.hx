package top.yunp.cms4py.app.pages.apis.actions.user;

import python.Dict;
import starlette.requests.Request;

@:build(hxasync.AsyncMacro.build())
class Profile extends Action {
	public function new() {
		super();
	}

	@async override function doAction(request:Request):Dict<String, Dynamic> {
		return Actions.createOkResult();
	}
}
