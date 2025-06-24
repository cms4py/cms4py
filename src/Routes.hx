package;
import python.lib.os.Path;
import python.Syntax;
import starlette.routing.Mount;
import starlette.routing.Route;
import starlette.staticfiles.StaticFiles;
import com.example.pages.Index;
import top.yunp.cms4py.web.Server;

class Routes {
    public static function createRoutes():Array<Route> {
        return [
            Syntax.callNamedUntyped(Mount, {path:"/static", app:Syntax.callNamedUntyped(StaticFiles, {directory:Path.join(Server.projectRoot, Server.web.get("staticRoot")), html:true})}),
            new Route("/", Index.page)
        ];
    }
}