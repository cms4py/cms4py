package com.example.pages;

import externals.starlette.requests.Request;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.web.routing.Page;
import externals.pyjwt.JWT;
import top.yunp.cms4py.framework.utils.ObjectUtils;

@:build(hxasync.AsyncMacro.build())
class Index extends Page {
	public function new() {}

	@async override public function execute(request:Request):Response {
		Logger.info(JWT.encode(ObjectUtils.toDict({a: 10}), "key", "HS256"));

		// var r = @await useCursor(@async cursor -> {
		// 	return @await cursor.select(db.user.login_name > 0, null, {limitby: [1, 2]});
		// });
		// Logger.info(r);
		return templateResponse(request, "index.html", {title: "Home"});
	}
}
