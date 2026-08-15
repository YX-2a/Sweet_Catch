from pathlib import Path
import shutil
import subprocess
import sys


lroot = Path(__file__).resolve().parent
groot = lroot.resolve().parent
outpt = groot / "output"

def create_desktop():
    with open(outpt / "sweet-catch.desktop", "w") as f:
        f.write("[Desktop Entry]\nType=Application\nName=Sweet Catch\nExec=./sweet-catch\nIcon=sweet-catch\nTerminal=false\nCategories=Entertainement;")

def build():
    if outpt.exists():
        shutil.rmtree(outpt)
    Path(outpt / "bin").mkdir(parents=True, exist_ok=True)
    args = [
            sys.executable,
            "-m",
            "nuitka",
    
            str(groot / "src" / "main.py"),

            "--onefile-no-compression",

            "--mode=onefile",
            "--enable-plugin=pyside6",
    
            f"--output-dir={outpt}",    
            f"--include-data-dir={groot / "data"}=data",
            f"--include-data-dir={groot / "config"}=config",
            
            "--include-data-files-external=data/textures/**",
            "--include-data-files-external=data/sounds/**",
            "--include-data-files-external=config/**",

            "--product-name=\"Sweet Catch\"",
            "--file-version=1.0",
            "--verbose",
            "--assume-yes-for-downloads"
    ]

    if sys.platform == "win32":
        args += ["--windows-console-mode=disable",f"--output-filename={outpt / "bin/Sweet Catch.exe"}", f"--windows-icon-from-ico={groot / "data" / "icons/win32/leaf.ico"}"]
    else:
        args += [f"--output-filename={outpt / "bin/sweet-catch"}"]

    subprocess.run(args,check=True)


if __name__ == "__main__":
    build()
    if (outpt / "main.onefile-build").exists():
        shutil.rmtree(outpt / "main.onefile-build")
    if (outpt / "main.dist").exists():
        shutil.rmtree(outpt / "main.dist")
    if (outpt / "main.build").exists():
        shutil.rmtree(outpt / "main.build")

    if sys.platform == "linux":
        shutil.coptree(groot / "data" / "icons/linux/hicolor",outpt / "icons/hicolor", dirs_exist_ok=True)
        create_desktop()
