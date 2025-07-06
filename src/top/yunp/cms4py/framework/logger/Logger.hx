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
package top.yunp.cms4py.framework.logger;

import top.yunp.cms4py.framework.web.Server;
import haxe.PosInfos;

class Logger {
	public static function trace(message:Dynamic, level:String = "TRACE", ?pos:PosInfos):Void {
		trace('${pos.fileName}:${pos.lineNumber} [${level}] ' + message);
	}

	public static function info(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.logLevelIndex <= LogLevel.INFO) {
			Logger.trace(message, "INFO", pos);
		}
	}

	public static function warn(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.logLevelIndex <= LogLevel.WARN) {
			Logger.trace(message, "WARN", pos);
		}
	}

	public static function error(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.logLevelIndex <= LogLevel.ERROR) {
			Logger.trace(message, "ERROR", pos);
		}
	}

	public static function debug(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.logLevelIndex <= LogLevel.DEBUG) {
			Logger.trace(message, "DEBUG", pos);
		}
	}
}
