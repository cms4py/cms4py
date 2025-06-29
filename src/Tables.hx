package;

import top.yunp.cms4py.framework.db.pydal.DAL;
import top.yunp.cms4py.framework.db.pydal.Field;

class Tables {
	public static function defineTables(db:DAL) {
		db.define_table(
            "user", 
            new Field("login_name"),
            new Field("nicename"),
            new Field("email"),
            new Field("password"),
            new Field("phone"),
            new Field("avatar"),
            new Field("gender"),
            new Field("is_super", "boolean"),
            new Field("created_at", "datetime"),
            new Field("updated_at", "datetime"),
            new Field("deleted_at", "datetime")
        );
	}
}
