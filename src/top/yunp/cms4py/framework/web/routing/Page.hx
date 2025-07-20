/*
 * MIT License
 *
 * Copyright (c) 2025 https://yunp.top
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
 * Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
 * AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
 * THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package top.yunp.cms4py.framework.web.routing;

import externals.pyjwt.JWT;
import externals.starlette.requests.Request;
import externals.starlette.responses.Response;
import haxe.exceptions.NotImplementedException;
import python.Lib;
import top.yunp.cms4py.framework.web.http.Context;
import top.yunp.cms4py.framework.web.exceptions.PageException;
import externals.starlette.responses.PlainTextResponse;
import top.yunp.cms4py.framework.logger.Logger;

@:build(hxasync.AsyncMacro.build())
class Page {
    @async public function execute(context:Context):Response {
        throw new NotImplementedException();
    }

    @:allow(top.yunp.cms4py.framework.web.routing.CRoute)
    @async final function __internal_call__(request:Request):Response {
        var resp:Response = null;
        try {
            var config = Server.web;
            var context = new Context(request);
            context.siteName = config.siteName;
            var jwt = request.cookies.get(config.sessionJwtName);
            if (jwt == null) {
                jwt = JWT.encode(Lib.anonAsDict({}), config.sessionJwtSecret, "HS256");
            }
            resp = @await execute(context);
            if (context.session.needUpdateJwt) {
                if (context.session.rememberMe) {
                    resp.set_cookie(config.sessionJwtName, context.session.jwt, config.sessionAge);
                } else {
                    resp.set_cookie(config.sessionJwtName, context.session.jwt);
                }
            }
        } catch (e:PageException) {
            if (e.response != null) {
                resp = e.response;
            } else {
                resp = new PlainTextResponse("Server internal error", 500);
                Logger.warn(e);
            }
        }
        return resp;
    }
}
