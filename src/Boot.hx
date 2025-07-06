package;

import python.Syntax;
import top.yunp.cms4py.ASGI;
import top.yunp.cms4py.framework.web.Server;

class Boot {
    static public function main() {
        Syntax.importModule('uvicorn');

        if (Syntax.code("__name__") == "__main__") {
            Syntax.callNamedUntyped(Syntax.code('uvicorn').run, {app: ASGI.app, host: "0.0.0.0", port:Server.web.serverPort});
        }
    }
}
