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

package top.yunp.cms4py.framework.web;

import externals.py.lang.PyWith;
import haxe.Json;
import python.Syntax;
import python.lib.Io;
import python.lib.os.Path;
import top.yunp.cms4py.framework.logger.LogLevel;

/**
 * Note: Logger can not be used in this class
 */
class Server {
	private static var _projectRoot:String = null;
	public static var projectRoot(get, null):String;

	private static function get_projectRoot():String {
		if (_projectRoot == null) {
			_projectRoot = Path.dirname(Path.dirname(Path.dirname(Syntax.code("__file__"))));
		}
		return _projectRoot;
	}

	private static var _web:IWebConfig = null;

	public static var web(get, null):IWebConfig;

	private static function get_web():IWebConfig {
		if (_web == null) {
			var content = PyWith.sync_with(Io.open(Path.join(projectRoot, "web.json"), "r"), it -> {
				return it.read();
			});
			_web = Json.parse(content);
			_web.logLevelIndex = LogLevel.getIndex(_web.logLevel);
		}
		return _web;
	}
}
