package top.yunp.cms4py.framework.db;

import externals.aiomysql.cursors.Cursor;
import top.yunp.cms4py.framework.db.PTable;
import python.Dict;
import top.yunp.cms4py.framework.db.PDAL;
import python.internal.AnonObject;

@:build(hxasync.AsyncMacro.build())
class PCursor {
    private var _cursor:Cursor = null;
    private var _modified = false;

    public function new(cursor:Cursor) {
        _cursor = cursor;
    }

    @async public function close() {
        @await _cursor.close();
    }

    @async public function execute(query:String, ?args:Dynamic):Dynamic {
        _modified = true;
        return @await _cursor.execute(query, args);
    }

    @async public function fetchall():Dynamic {
        return @await _cursor.fetchall();
    }

    @async public function count(query:Dynamic) {
        var db = PDAL.getInstance().op;
        var rows = @await _cursor.execute(db.query(query).count());
        if (rows != 1) {
            return 0;
        }
        var resultSet = @await fetchall();
        var first:Dict<String, Dynamic> = resultSet[0];
        return first.iterator().next();
    }

    @async public function isempty(query:Dynamic):Bool {
        return (@await count(query)) <= 0;
    }

    @async public function select(query:Dynamic, ?fields:Array<Dynamic>, ?options:Dynamic):Array<Dynamic> {
        var db = PDAL.getInstance().op;
        @await _cursor.execute(db.query(query).select(fields, options));
        var list:Array<Dynamic> = @await fetchall();
        return list.map(t -> new AnonObject(t));
    }

    @async public function selectOne(query:Dynamic, ?fields:Array<Dynamic>):Dynamic {
        var result = @await select(query, fields, {limitby:[0, 1]});
        if (result.length > 0) {
            return result[0];
        }
        return null;
    }

    public var modified(get, null):Bool;

    private function get_modified():Bool {
        return _modified;
    }

    @async public function insert(table:PTable, data:Dynamic):Int {
        return @await execute(table.insert(data));
    }

    @async public function delete(query:Dynamic):Int {
        var db = PDAL.getInstance().op;
        return @await execute(db.query(query).delete());
    }

    @async public function update(query:Dynamic, data:Dynamic):Int {
        var db = PDAL.getInstance().op;
        return @await execute(db.query(query).update(data));
    }
}
