package top.yunp.cms4py.framework.web;

import top.yunp.cms4py.framework.logger.LogLevel;
import python.lib.os.Path;
import python.Syntax;
import python.lib.Json;
import python.lib.Io;
import python.Dict;

class Server {
	private static var _projectRoot:String = null;
	public static var projectRoot(get, null):String;

	private static function get_projectRoot():String {
		if (_projectRoot == null) {
			_projectRoot = Path.dirname(Path.dirname(Path.dirname(Syntax.code("__file__"))));
		}
		return _projectRoot;
	}

	private static var _web:Dict<String, Dynamic> = null;

	public static var web(get, null):Dict<String, Dynamic>;

	public static function get_web():Dict<String, Dynamic> {
		if (_web == null) {
			var f = Io.open(Path.join(projectRoot, "web.json"), "r");
			var content = Syntax.field(f, "read")();
			f.close();
			_web = Json.loads(content);
			_web.set("logLevelIndex", LogLevel.getIndex(_web.get("logLevel")));
		}
		return _web;
	}
}
