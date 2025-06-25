package;
import top.yunp.cms4py.db.pydal.DAL;
import top.yunp.cms4py.db.pydal.Field;

class Tables {
    public static function defineTables(db:DAL) {
        db.define_table("users", new Field("name"));
    }
}