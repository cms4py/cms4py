package top.yunp.cms4py.app.pages.apis.actions;

import python.Dict;

class Actions {
	public static final CODE_OK = 0;
	public static final CODE_ACTION_NOT_FOUND = 8001;

	public static function createOkResult(?result:Dynamic) {
		return createResult(CODE_OK, "OK", result);
	}

	public static function createResult(code:Int, message:String, ?result:Dynamic):Dict<String, Dynamic> {
		var d = new Dict<String, Dynamic>();
		d.set("code", code);
		d.set("message", message);
		if (result != null) {
			d.set("result", result);
		}
		return d;
	}
}
