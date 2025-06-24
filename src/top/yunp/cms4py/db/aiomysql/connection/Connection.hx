package top.yunp.cms4py.db.aiomysql.connection;
import top.yunp.cms4py.db.aiomysql.cursors.Cursor;

@:pythonImport("aiomysql.connection", "Connection")
extern class Connection {
    @async public function cursor():Cursor;
}