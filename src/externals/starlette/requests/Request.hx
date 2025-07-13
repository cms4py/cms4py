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

package externals.starlette.requests;

import python.Dict;

@:pythonImport("starlette.requests", "Request")
extern class Request {
    public final method:String;
    public final url:Dynamic;
    public final client:Dynamic;
    public final path_params:Dict<String, String>;
    public final query_params:Dict<String, String>;
    public final headers:Dict<String, String>;
    public final cookies:Dict<String, String>;

    @async public function body():Dynamic;

    @async public function form():Dict<String, Dynamic>;

    @async public function json():Dynamic;

    @async public function stream():Dynamic;
}
