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

package com.example.myapp.apis.user;

import top.yunp.cms4py.framework.web.routing.apis.actions.Action;
import top.yunp.cms4py.framework.web.http.Context;
import externals.pydal.validators.CRYPT;
import python.Tuple.Tuple1;
import python.Tuple.Tuple2;
import top.yunp.cms4py.framework.logger.Logger;
import com.example.myapp.apis.exceptions.ParametersError;
import python.Dict;
import com.example.myapp.apis.exceptions.InvalidLogin;

@:build(hxasync.AsyncMacro.build())
class SignIn extends Action {
    public function new() {
        super();
    }

    @async override public function doAction(context:Context):Dynamic {
        var form = @await context.request.form();
        var username = form.get("username");
        var password = form.get("password");
        var rememberMe = form.get("remember_me");

        if (username == null || password == null) {
            throw new ParametersError();
        }

        var crypt:Dynamic = new CRYPT();
        var pt:Tuple1<Dynamic> = crypt(password);
        var p = pt._1;
        var user:Dynamic = @await context.useCursor(@async c -> {
            var u = @await c.selectOne(context.db.user.login_name == username);
            if (u != null && p == u.password) {
                return u;
            }
            return null;
        });

        if (user == null) {
            throw new InvalidLogin();
        }

        var userid = user.id;
        context.session.userid = userid;
        if (rememberMe != null) {
            context.session.rememberMe = true;
        }
        return Action.createOkResult({id:userid});
    }
}
