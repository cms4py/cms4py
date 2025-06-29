package top.yunp.cms4py.framework.logger;

class LogLevel {
	public static final ALL = 0;
	public static final DEBUG = 1;
	public static final INFO = 2;
	public static final WARN = 3;
	public static final ERROR = 4;

	private static final levelStrings = ["ALL", "DEBUG", "INFO", "WARN", "ERROR"];

	public static function getLabel(level:Int):String {
		return levelStrings[level];
	}

	public static function getIndex(level:String):Int {
		for (i in 0...levelStrings.length) {
			if (levelStrings[i].toLowerCase() == level.toLowerCase()) {
				return i;
			}
		}
		return 2;
	}
}
