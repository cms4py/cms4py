package com.example.pages;

import top.yunp.cms4py.framework.web.http.Context;
import externals.starlette.requests.Request;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.web.routing.Page;
import externals.pyjwt.JWT;
import top.yunp.cms4py.framework.utils.ObjectUtils;

@:build(hxasync.AsyncMacro.build())
class Index extends Page {
	public function new() {}

	@async override public function execute(context:Context):Response {
		Logger.info(JWT.encode(ObjectUtils.toDict({a: 10}), "key", "HS256"));
		// Logger.info(request.cookies);
	

		// var r = @await useCursor(@async cursor -> {
		// 	return @await cursor.select(db.user.login_name > 0, null, {limitby: [1, 2]});
		// });
		// Logger.info(r);
		return context.templateResponse("index.html", {title: "Home"});
	}
}
