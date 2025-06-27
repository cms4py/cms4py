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
            // @await cursor.insert(db.users, {name: "OK"});
//            return @await cursor.select(db.users.id > 0);
//            return @await cursor.delete(db.users.id == 4);
//            return @await cursor.update(db.users.id == 2, {name:"Hello"});
//            return @await cursor.selectOne(db.users.id == 2);
            return @await cursor.select(db.users.id > 0, null, {limitby:[1, 2]});
        });
        Logger.info(r);
        return templateResponse(request, "index.html", {content: "Hello"});
    }
}
