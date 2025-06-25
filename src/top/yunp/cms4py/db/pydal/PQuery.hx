package top.yunp.cms4py.db.pydal;

import top.yunp.cms4py.lib.FuncTools;

class PQuery {

    private var _dalQuery:Dynamic;

    public function new(dalQuery) {
        _dalQuery = dalQuery;
    }

    public function select(?fields:Array<Dynamic>, ?options:Dynamic) {
        var s = Reflect.field(_dalQuery, "_select");
        return FuncTools.call(s, fields, options);
    }
}