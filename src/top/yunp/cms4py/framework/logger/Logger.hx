package top.yunp.cms4py.framework.logger;

import top.yunp.cms4py.framework.web.Server;
import haxe.PosInfos;

class Logger {
	public static function trace(message:Dynamic, level:String = "TRACE", ?pos:PosInfos):Void {
		trace('${pos.fileName}:${pos.lineNumber} [${level}] ' + message);
	}

	public static function info(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.get("logLevelIndex") <= LogLevel.INFO) {
			Logger.trace(message, "INFO", pos);
		}
	}

	public static function warn(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.get("logLevelIndex") <= LogLevel.WARN) {
			Logger.trace(message, "WARN", pos);
		}
	}

	public static function error(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.get("logLevelIndex") <= LogLevel.ERROR) {
			Logger.trace(message, "ERROR", pos);
		}
	}

	public static function debug(message:Dynamic, ?pos:PosInfos):Void {
		if (Server.web.get("logLevelIndex") <= LogLevel.DEBUG) {
			Logger.trace(message, "DEBUG", pos);
		}
	}
}
