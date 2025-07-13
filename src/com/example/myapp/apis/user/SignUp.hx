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

import externals.pydal.validators.CRYPT;
import externals.pymysql.err.IntegrityError;
import python.lib.Re;
import python.Syntax;
import top.yunp.cms4py.app.pages.apis.actions.Action;
import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.web.http.Context;

@:build(hxasync.AsyncMacro.build())
class SignUp extends Action {
    public function new() {
        super();
    }

    @async override public function doAction(context:Context):Dynamic {
        var form = @await context.request.form();
        var username:String = form.get("username");
        var password:String = form.get("password");

        if (username == null || password == null) {
            return Action.createResult(ResultCode.CODE_PARAMETERS_ERROR, "Parameters error");
        }

        var actionResult:Dynamic = null;
        @await context.useCursor(@async c -> {
            var crypt:Dynamic = new CRYPT();
            var p = crypt(password);
            try {
                var insertUserResult = @await c.insert(context.db.user, {login_name:username, password:Syntax.arrayAccess(p, 0)});
                var user = @await c.selectOne(context.db.user.login_name == username);
                if (user != null) {
                    context.session.userid = '${user.get("id")}';
                    actionResult = Action.createOkResult({id:user.get("id")});
                } else {
                    actionResult = Action.createErrorResult();
                }
            } catch (e:IntegrityError) {
                if (e.args._1 == ResultCode.CODE_MYSQL_DUPLICATE_ENTRY) {
                    var m = Re.search("Duplicate entry '\\w+' for key '(\\w+)'", e.args._2, Re.I);
                    if (m != null) {
                        var fieldName = m.group(1);
                        actionResult = Action.createResult(ResultCode.CODE_MYSQL_DUPLICATE_ENTRY, "Duplicate entry", {field:fieldName});
                    }
                } else {
                    Logger.warn(e);
                }
            }
        });
        if (actionResult == null) {
            actionResult = Action.createErrorResult();
        }
        return actionResult;
    }
}
