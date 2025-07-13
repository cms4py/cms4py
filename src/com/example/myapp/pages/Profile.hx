package com.example.myapp.pages;

import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.web.http.Context;
import top.yunp.cms4py.framework.web.routing.Page;

@:build(hxasync.AsyncMacro.build())
class Profile extends Page {
    public function new() {}

    @async override function execute(context:Context):Response {
        return context.render("profile.html", {title: "我的信息"});
    }
}
