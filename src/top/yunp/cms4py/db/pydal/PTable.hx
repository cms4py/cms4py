package top.yunp.cms4py.db.pydal;

class PTable {

    private var _table:Dynamic = null;
    private var _op:PTableOp;

    public function new(table:Dynamic) {
        _table = table;
        _op = new PTableOp(this);
    }

    public function field(name:String):Dynamic {
        return Reflect.field(_table, name);
    }

    public function f(name:String):Dynamic {
        return field(name);
    }

    public var op(get, null):PTableOp;

    private function get_op():PTableOp {
        return _op;
    }

}

abstract PTableOp(PTable) {
    public inline function new(t:PTable) {
        this = t;
    }

    @:op([])
    @:op(a.b)
    public function field(name:String) {
        return this.field(name);
    }
}