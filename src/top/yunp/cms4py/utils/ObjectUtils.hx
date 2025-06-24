package top.yunp.cms4py.utils;

import python.Dict;

class ObjectUtils {
    public static function toDict(obj:Dynamic):Dict<String, Dynamic> {
        var r = new Dict<String, Dynamic>();
        for (f in Reflect.fields(obj)) {
            r.set(f, Reflect.getProperty(obj, f));
        }
        return r;
    }
}