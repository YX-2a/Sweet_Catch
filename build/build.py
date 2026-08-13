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

    args = [
            sys.executable,
            "-m",
            "nuitka",
    
            str(groot / "main.py"),
    
            "--mode=onefile",
            "--enable-plugin=pyside6",
    
            f"--output-dir={outpt}",    
            f"--include-data-dir={groot / 'sounds'}=sounds",
            f"--include-data-dir={groot / 'textures'}=textures",
            f"--include-data-file={groot / 'game.settings'}=game.settings",
            
            "--include-data-files-external=sounds/**",
            "--include-data-files-external=textures/**",
            "--include-data-files-external=game.settings",

            "--product-name=\"Sweet Catch\"",
            "--file-version=1.0",
            "--verbose",
            "--assume-yes-for-downloads"
    ]

    if sys.platform == "win32":
        args += ["--windows-console-mode=disable","--output-filename=Sweet Catch.exe", f"--windows-icon-from-ico={groot / "icons/win32/leaf.ico"}"]
    else:
        args += ["--output-filename=sweet-catch"]

    subprocess.run(args,check=True)


if __name__ == "__main__":
    create_desktop()
    #build()
    if (outpt / "main.onefile-build").exists():
        shutil.rmtree(outpt / "main.onefile-build")
    if (outpt / "main.dist").exists():
        shutil.rmtree(outpt / "main.dist")
    if (outpt / "main.build").exists():
        shutil.rmtree(outpt / "main.build")

    if sys.platform == "linux":
        shutil.coptree(groot / "icons/linux/hicolor",outpt / "icons/hicolor", dirs_exist_ok=True)
        create_desktop()
