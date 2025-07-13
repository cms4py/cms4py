package externals.pymysql.err;

@:pythonImport("pymysql.err", "Error")
extern class Error extends MySQLError {
    public function new();
}
