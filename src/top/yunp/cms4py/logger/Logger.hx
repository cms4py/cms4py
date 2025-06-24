package top.yunp.cms4py.logger;
import haxe.PosInfos;
import top.yunp.cms4py.logger.Logger;

class Logger {
    public static function trace(message:Dynamic, level:String = "INFO", ?pos:PosInfos):Void {
        trace('${pos.fileName}:${pos.lineNumber} [${level}] ' + message);
    }

    public static function info(message:Dynamic, ?pos:PosInfos):Void {
        Logger.trace(message, "INFO", pos);
    }

    public static function warn(message:Dynamic, ?pos:PosInfos):Void {
        Logger.trace(message, "WARN", pos);
    }

    public static function error(message:Dynamic, ?pos:PosInfos):Void {
        Logger.trace(message, "ERROR", pos);
    }

    public static function debug(message:Dynamic, ?pos:PosInfos):Void {
        Logger.trace(message, "DEBUG", pos);
    }
}
