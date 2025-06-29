package top.yunp.cms4py.framework.lib;

import python.Dict;
import python.Syntax;
import top.yunp.cms4py.framework.utils.ObjectUtils;

@:build(hxasync.AsyncMacro.build())
class FuncTools {
	private static function callNamed1(func:Dynamic, options:Dict<String, Dynamic>):Dynamic {
		return Syntax.code("func(**options)");
	}

	private static function callNamed2(func:Dynamic, options:Dynamic) {
		return callNamed1(func, ObjectUtils.toDict(options));
	}

	private static function callNamed3(func:Dynamic, args:Array<Dynamic>, options:Dict<String, Dynamic>) {
		return Syntax.code("func(*args,**options)");
	}

	private static function callNamed4(func:Dynamic, args:Array<Dynamic>, options:Dynamic) {
		return callNamed3(func, args, ObjectUtils.toDict(options));
	}

	public static function call(func:Dynamic, ?args:Array<Dynamic>, ?kwargs:Dynamic):Dynamic {
		return callNamed4(func, args != null ? args : [], kwargs != null ? kwargs : {});
	}

	public static function callNamed(func:Dynamic, options:Dynamic):Dynamic {
		return callNamed2(func, options != null ? options : {});
	}
}
