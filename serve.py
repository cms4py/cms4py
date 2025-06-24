import uvicorn
import sys
import json
import subprocess


def main():
    if 'compile' in sys.argv:
        print("Compiling haxe project...")
        if subprocess.run(["haxe", "build.hxml"]).returncode > 0:
            print("Failed to compile project")
            return
    with open("web.json") as f:
        web = json.load(f)
        uvicorn.run(
            app="out.python.server:top_yunp_cms4py_ASGI.app",
            host="0.0.0.0",
            port=web["serverPort"],
            workers=1
        )


if __name__ == "__main__":
    main()
    
