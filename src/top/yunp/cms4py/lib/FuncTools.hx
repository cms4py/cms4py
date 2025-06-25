package top.yunp.cms4py.lib;
import python.Dict;
import python.Syntax;
import top.yunp.cms4py.utils.ObjectUtils;

class FuncTools {
    public static function callNamed1(func:Dynamic, options:Dict<String, Dynamic>):Dynamic {
        return Syntax.code("func(**options)");
    }

    public static function callNamed2(func:Dynamic, options:Dynamic) {
        return callNamed1(func, ObjectUtils.toDict(options));
    }

    public static function callNamed3(func:Dynamic, args:Array<Dynamic>, options:Dict<String, Dynamic>) {
        return Syntax.code("func(*args,**options)");
    }


    public static function callNamed4(func:Dynamic, args:Array<Dynamic>, options:Dynamic) {
        return callNamed3(func, args, ObjectUtils.toDict(options));
    }

    public static function call(func:Dynamic, ?args:Array<Dynamic>, ?kwargs:Dynamic) {
        return callNamed4(func, args != null ? args : [], kwargs != null ? kwargs : {});
    }
}