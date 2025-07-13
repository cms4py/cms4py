package externals.pymysql.err;
import python.Exceptions.Exception;
import python.Tuple.Tuple2;

@:pythonImport("pymysql.err", "MySQLError")
extern class MySQLError extends Exception {
    public function new();

    public final args:Tuple2<Int, Dynamic>;
}
