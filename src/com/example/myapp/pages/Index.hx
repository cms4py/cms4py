package com.example.myapp.pages;

import externals.pyjwt.JWT;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.utils.ObjectUtils;
import top.yunp.cms4py.framework.web.http.Context;
import top.yunp.cms4py.framework.web.routing.Page;

@:build(hxasync.AsyncMacro.build())
class Index extends Page {
	public function new() {}

	@async override public function execute(context:Context):Response {
		Logger.info(Date.now().getTime());

		// context.session.userid = "10";
		// Logger.info(JWT.encode(ObjectUtils.toDict({a: 10}), "key", "HS256"));
		// Logger.info(request.cookies);

		// var r = @await useCursor(@async cursor -> {
		// 	return @await cursor.select(db.user.login_name > 0, null, {limitby: [1, 2]});
		// });
		// Logger.info(r);

		var u = @await context.useCursor(@async c -> {
			return @await c.select(context.db.user.id > 0);
		});
		Logger.info(u);
		return context.render("index.html", {title: "主页"});
	}
}
