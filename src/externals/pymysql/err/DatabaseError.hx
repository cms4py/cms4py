package externals.pymysql.err;

@:pythonImport("pymysql.err", "DatabaseError")
extern class DatabaseError extends Error {
    public function new();
}
