package top.yunp.cms4py.framework.web.templating;
import starlette.templating.Jinja2Templates;
import starlette.responses.HTMLResponse;
import starlette.requests.Request;
import top.yunp.cms4py.framework.utils.ObjectUtils;
import python.lib.os.Path;
import top.yunp.cms4py.framework.web.Server;

class Templates extends Jinja2Templates {

    public function new(directory:String) {
        super(directory);
    }

    public function response(request:Request, name:String, ?context:Dynamic):HTMLResponse {
        if (context != null) {
            return TemplateResponse(request, name, ObjectUtils.toDict(context));
        } else {
            return TemplateResponse(request, name);
        }

    }

    private static var _instance:Templates = null;

    public static function getInstance():Templates {
        if (_instance == null) {
            _instance = new Templates(Path.join(Server.projectRoot, Server.web.get("templateRoot")));
        }
        return _instance;
    }
}