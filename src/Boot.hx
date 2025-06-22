package;

import top.yunp.cms4py.AsgiAppFactory;
import python.Syntax;

class Boot {
	static public function main() {
		Syntax.importModule('uvicorn');

		if (Syntax.code("__name__") == "__main__") {
			Syntax.callNamedUntyped(Syntax.code('uvicorn').run, {app: AsgiAppFactory.createAsgiApp(), host: "0.0.0.0"});
		}
	}
}
