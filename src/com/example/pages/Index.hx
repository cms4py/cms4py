package com.example.pages;
import starlette.requests.Request;
import starlette.responses.Response;
import top.yunp.cms4py.logger.Logger;
import top.yunp.cms4py.web.routing.Page;

@:build(hxasync.AsyncMacro.build())
class Index extends Page {

    public function new() {}

    @async override public function execute(request:Request):Response {
        var r = @await useCursor(@async cursor -> {
            @await cursor.execute(db(db.users.id > 0).select());
            return @await cursor.fetchall();
        });
        Logger.info(r);
        return templateResponse(request, "index.html", {content:"Hello"});
    }
}