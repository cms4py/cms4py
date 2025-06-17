import subprocess

if __name__ == '__main__':
    p = subprocess.run(['haxe', 'build.hxml'], shell=True)
    if p.returncode != 0:
        print('Build failed')
        exit(1)

    subprocess.run(['python', 'out/python/main.py'], shell=True)
