package top.yunp.cms4py.db.aiomysql.cursors;

@:pythonImport("aiomysql.cursors", "Cursor")
extern class Cursor {
    @async public function execute(sql:String):Dynamic;

    @async public function fetchone():Dynamic;

    @async public function fetchall():Dynamic;

    @async public function close():Dynamic;
}