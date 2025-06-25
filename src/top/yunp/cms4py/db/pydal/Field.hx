package top.yunp.cms4py.db.pydal;

@:pythonImport("pydal", "Field")
extern class Field {
    public function new(fieldname:String, ?type:String);
}