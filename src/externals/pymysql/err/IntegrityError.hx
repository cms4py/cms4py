package externals.pymysql.err;

@:pythonImport("pymysql.err", "IntegrityError")
extern class IntegrityError extends DatabaseError {
    public function new();
}
