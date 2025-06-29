package;

import top.yunp.cms4py.app.pages.apis.actions.user.Profile;
import top.yunp.cms4py.app.pages.apis.API;
import com.example.pages.Index;
import top.yunp.cms4py.framework.web.routing.CRoute;

class Routes {
    public static function configRoutes():Array<CRoute> {

        var apis = new API();
        apis.addAction("user.profile.aspx", new Profile());

        return [
            new CRoute("/", new Index()),
            new CRoute("/apis/{action}", apis)
        ];
    }
}