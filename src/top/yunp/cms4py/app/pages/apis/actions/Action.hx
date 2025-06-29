package top.yunp.cms4py.app.pages.apis.actions;

import python.Exceptions.NotImplementedError;
import python.Dict;
import starlette.requests.Request;

@:build(hxasync.AsyncMacro.build())
class Action {
	public function new() {}

	@async public function doAction(request:Request):Dict<String, Dynamic> {
		throw new NotImplementedError();
	}
}
