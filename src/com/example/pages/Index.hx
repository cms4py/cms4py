package com.example.pages;

import externals.starlette.requests.Request;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.web.routing.Page;

@:build(hxasync.AsyncMacro.build())
class Index extends Page {
	public function new() {}

	@async override public function execute(request:Request):Response {
		var r = @await useCursor(@async cursor -> {
			return @await cursor.select(db.user.login_name > 0, null, {limitby: [1, 2]});
		});
		Logger.info(r);
		return templateResponse(request, "index.html", {title: "Home"});
	}
}
