package com.example.pages;
import starlette.requests.Request;
import starlette.responses.Response;
import top.yunp.cms4py.db.DbConnector;
import top.yunp.cms4py.logger.Logger;
import top.yunp.cms4py.templating.Templates;

@:build(hxasync.AsyncMacro.build())
class Index {
    @async public static function page(request:Request):Response {
        @await DbConnector.getInstance().use(@async (cursor) -> {
            var r = @await cursor.execute("select * from users");
            r = @await cursor.fetchall();
            Logger.info(r);
        });
        return Templates.getInstance().response(request, "index.html", {content:"Hello"});
    }
}