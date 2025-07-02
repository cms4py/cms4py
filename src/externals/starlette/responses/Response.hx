package externals.starlette.responses;

import python.Dict;

@:pythonImport("starlette.responses", "Response")
extern class Response {
	public function new(content:String, ?status_code:Int, ?headers:Dict<String, String>, ?media_type:String);

	public function set_cookie(
        key:String, 
        value:String, 
        ?max_age:Int, 
        ?expires:Int, 
        ?path:String, 
        ?domain:String, 
        ?secure:Bool, 
        ?httponly:Bool,
		?samesite:String, 
        ?partitioned:Bool
    ):Void;
}
