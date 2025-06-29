package;
import com.example.pages.Index;
import top.yunp.cms4py.framework.web.routing.CRoute;

class Routes {
    public static function configRoutes():Array<CRoute> {
        return [
            new CRoute("/", new Index())
        ];
    }
}