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

package top.yunp.cms4py.framework.web.http;

import top.yunp.cms4py.framework.lib.FuncTools;
import externals.starlette.responses.PlainTextResponse;
import haxe.Json;
import externals.starlette.responses.JSONResponse;
import python.Dict;
import top.yunp.cms4py.framework.db.DbConnector;
import top.yunp.cms4py.framework.db.PDAL;
import top.yunp.cms4py.framework.db.PCursor;
import top.yunp.cms4py.framework.web.templating.Templates;
import python.lib.Builtins;
import externals.starlette.requests.Request;
import externals.starlette.responses.Response;

@:build(hxasync.AsyncMacro.build())
class Context {
    public function new(request:Request) {
        this._request = request;
    }

    private var _request:Request;

    public var request(get, never):Request;

    private function get_request():Request {
        return _request;
    }

    public var siteName(get, set):String;

    private function get_siteName() {
        if (Builtins.hasattr(request, "siteName")) {
            return (request : Dynamic).siteName;
        } else {
            return "";
        }
    }

    private function set_siteName(value:String) {
        (request : Dynamic).siteName = value;
        return value;
    }

    public function render(name:String, ?context:Dynamic):Response {
        return Templates.getInstance().response(request, name, context);
    }

    public function json(data:Dynamic):Response {
        return FuncTools.callNamed(PlainTextResponse, {content: Json.stringify(data), media_type: "application/json"});
    }

    public var db(get, null):PDALOp;

    private function get_db():PDALOp {
        return PDAL.getInstance().op;
    }

    @async public function useCursor<R>(handler:(cursor:PCursor) -> R):R {
        return @await DbConnector.getInstance().use(handler);
    }

    public var method(get, null):String;

    private function get_method() {
        return request.method;
    }

    public var url(get, null):Dynamic;

    private function get_url() {
        return request.url;
    }

    public var client(get, null):Dynamic;

    private function get_client() {
        return request.client;
    }

    public var path_params(get, null):Dict<String, String>;

    private function get_path_params() {
        return request.path_params;
    }

    public var query_params(get, null):Dict<String, String>;

    private function get_query_params() {
        return request.query_params;
    }

    public var headers(get, null):Dict<String, String>;

    private function get_headers() {
        return request.headers;
    }

    public var cookies(get, null):Dict<String, String>;

    private function get_cookies() {
        return request.cookies;
    }

    public var session(get, null):JWTSession;

    private var _session:JWTSession = null;

    private function get_session() {
        if (_session == null) {
            _session = new JWTSession(this);
        }
        return _session;
    }
}
