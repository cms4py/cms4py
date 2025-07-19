package com.example.myapp.pages;

import top.yunp.cms4py.framework.web.http.Context;
import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.web.routing.Page;
import top.yunp.cms4py.framework.web.Server;
import Math;

@:build(hxasync.AsyncMacro.build())
class Sign extends Page {
    public function new() {}

    @async override function execute(context:Context):Response {
        return context.render(
            "sign.html",
            {
                title: "登录/注册",
                web:Server.web,
                sessionAgeDays:Math.round(Server.web.sessionAge / 3600 / 24)
            }
        );
    }
}
