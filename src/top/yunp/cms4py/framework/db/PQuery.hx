package top.yunp.cms4py.framework.db;

import top.yunp.cms4py.framework.logger.Logger;
import top.yunp.cms4py.framework.lib.FuncTools;

class PQuery {
    private var _dalQuery:Dynamic;

    public function new(dalQuery) {
        _dalQuery = dalQuery;
    }

    public function select(?fields:Array<Dynamic>, ?options:Dynamic):String {
        var sql = FuncTools.call(_dalQuery._select, fields, options);
        Logger.debug(sql);
        return sql;
    }

    public function count():String {
        var sql = _dalQuery._count();
        Logger.debug(sql);
        return sql;
    }

    public function delete():String {
        var sql = _dalQuery._delete();
        Logger.debug(sql);
        return sql;
    }

    public function update(data):String {
        var sql = FuncTools.callNamed(_dalQuery._update, data);
        Logger.debug(sql);
        return sql;
    }
}
