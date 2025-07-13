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

package top.yunp.cms4py.framework.web.routing.apis;

import externals.starlette.responses.Response;
import top.yunp.cms4py.framework.web.routing.apis.actions.Action;
import top.yunp.cms4py.framework.web.http.Context;
import top.yunp.cms4py.framework.web.routing.Page;
import top.yunp.cms4py.framework.web.exceptions.APIException;

@:build(hxasync.AsyncMacro.build())
class API extends Page {
    public function new() {}

    private var _actions = new Map<String, Action>();

    public function addAction(name:String, action:Action) {
        _actions.set(name, action);
    }

    public var actions(get, never):Map<String, Action>;

    private function get_actions():Map<String, Action> {
        return _actions;
    }

    @async override function execute(context:Context):Response {
        var actionName = context.path_params.get("action");
        var result:Dynamic = null;
        if (actions.exists(actionName)) {
            try {
                result = @await actions.get(actionName).doAction(context);
            } catch (e:APIException) {
                result = e.result;
            }
        } else {
            result = Action.createResult(Action.CODE_ACTION_NOT_FOUND, "Action not found");
        }
        return context.json(result);
    }
}
