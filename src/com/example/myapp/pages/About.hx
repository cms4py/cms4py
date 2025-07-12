package com.example.myapp.pages;

import top.yunp.cms4py.framework.web.http.Context;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.web.routing.Page;

@:build(hxasync.AsyncMacro.build())
class About extends Page {
	public function new() {}

	@async override function execute(context:Context):Response {
		return context.render("about.html", {title: "关于"});
	}
}
