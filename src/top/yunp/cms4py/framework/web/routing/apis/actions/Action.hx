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

package top.yunp.cms4py.framework.web.routing.apis.actions;

import python.Exceptions.NotImplementedError;
import top.yunp.cms4py.framework.web.http.Context;

@:build(hxasync.AsyncMacro.build())
class Action {
    public function new() {}

    @async public function doAction(context:Context):Dynamic {
        throw new NotImplementedError();
    }

    public static final CODE_OK = 0;
    public static final CODE_ERROR = 1;
    public static final CODE_ACTION_NOT_FOUND = 8001;

    public static function createOkResult(?result:Dynamic) {
        return createResult(CODE_OK, "OK", result);
    }

    public static function createErrorResult(?result:Dynamic) {
        return createResult(CODE_ERROR, "Error", result);
    }

    public static function createResult(code:Int, message:String, ?result:Dynamic):Dynamic {
        var d:Dynamic = {code: code, message: message};
        if (result != null) {
            d.result = result;
        }
        return d;
    }
}
