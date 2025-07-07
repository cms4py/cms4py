package com.example.pages;

import top.yunp.cms4py.framework.web.http.Context;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.web.routing.Page;

@:build(hxasync.AsyncMacro.build())
class Sign extends Page {
	public function new() {}

	@async override function execute(context:Context):Response {
		return context.render("sign.html", {title: "登录/注册"});
	}
}
