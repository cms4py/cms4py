package top.yunp.cms4py.framework.db.aiomysql;

@:pythonImport("aiomysql")
extern class Aiomysql {
    public static function create_pool():Dynamic;
}