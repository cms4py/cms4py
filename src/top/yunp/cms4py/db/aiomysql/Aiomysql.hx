package top.yunp.cms4py.db.aiomysql;

@:pythonImport("aiomysql")
extern class Aiomysql {
    public static function create_pool():Dynamic;
}