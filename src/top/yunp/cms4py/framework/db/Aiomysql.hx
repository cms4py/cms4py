package top.yunp.cms4py.framework.db;

@:pythonImport("aiomysql")
extern class Aiomysql {
    public static function create_pool():Dynamic;
}