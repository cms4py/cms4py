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

import top.yunp.cms4py.framework.logger.Logger;
import haxe.Exception;
import python.Lib;
import externals.pyjwt.JWT;

/**
 * JWT Session only store the userid
 */
class JWTSession {
    private var _context:Context;
    private var _jwt:String;
    private var _needUpdateJwt = false;

    public function new(context:Context) {
        _context = context;
        _jwt = context.cookies.get(Server.web.sessionJwtName);
        if (_jwt == null) {
            _needUpdateJwt = true;
            return;
        }

        try {
            var payload = JWT.decode(_jwt, Server.web.sessionJwtSecret, "HS256");
            if ((payload.get("exp") ?? 0) < Date.now().getTime()) {
                _needUpdateJwt = true;
                return;
            }

            _userid = payload.get("userid");
        } catch (e:Exception) {}
    }

    private var _exp:Float = 0;

    public var exp(get, null):Float;

    private function get_exp() {
        return _exp;
    }

    public var needUpdateJwt(get, null):Bool;

    private function get_needUpdateJwt() {
        return _needUpdateJwt;
    }

    public var userid(get, set):String;

    private var _userid:String = null;

    private function set_userid(value:String):String {
        if (_userid != value) {
            _userid = value;
            _exp = Date.now().getTime() + Server.web.sessionAge * 1000;
            _needUpdateJwt = true;
        }
        return _userid;
    }

    private function get_userid():String {
        return _userid;
    }

    /**
	 * Generate new jwt when need
	 */
    public var jwt(get, null):String;

    private function get_jwt():String {
        if (_needUpdateJwt) {
            return JWT.encode(Lib.anonAsDict({userid: userid, exp: exp}), Server.web.sessionJwtSecret, "HS256");
        } else {
            return _jwt;
        }
    }

    private var _rememberMe = false;

    public var rememberMe(get, set):Bool;

    private function set_rememberMe(value:Bool):Bool {
        _rememberMe = value;
        return _rememberMe;
    }

    private function get_rememberMe():Bool {
        return _rememberMe;
    }
}
