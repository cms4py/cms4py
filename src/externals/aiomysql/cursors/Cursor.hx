package externals.aiomysql.cursors;

@:pythonImport("aiomysql.cursors", "Cursor")
extern class Cursor {
    @async public function execute(query:String, ?args:Dynamic):Dynamic;

    @async public function executemany(query:String, args:Dynamic):Dynamic;

    @async public function fetchone():Dynamic;

    @async public function fetchmany(?size:Int):Dynamic;

    @async public function fetchall():Dynamic;

    @async public function close():Dynamic;

    public var description:Dynamic;

    public var rowcount:Int;

    public var rownumber:Int;

    public var arraysize:Int;

    public var lastrowid:Int;

    public var closed:Bool;
}