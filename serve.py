import uvicorn
import sys
import subprocess

if __name__ == "__main__":
    if 'compile' in sys.argv:
        print("Compiling haxe project...")
        subprocess.run(["haxe", "build.hxml"])
    uvicorn.run(app="serve_handler:app", workers=1)
