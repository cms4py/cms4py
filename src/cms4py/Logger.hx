package cms4py;
import haxe.PosInfos;

class Logger {
	public static function trace(message:Dynamic, ?pos:PosInfos):Void {
		trace('${pos.fileName}:${pos.lineNumber} ' + message);
	}
}
