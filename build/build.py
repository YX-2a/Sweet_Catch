from pathlib import Path
import shutil
import subprocess
import sys


lroot = Path(__file__).resolve().parent
groot = lroot.resolve().parent
outpt = groot / "output"


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
        args += ["--windows-console-mode=disable","--output-filename=Sweet Catch.exe", f"--windows-icon-from-ico={groot / "leaf.ico"}"]
    else:
        args += ["--output-filename=Sweet Catch", f"--linux-icon={groot / "leaf.ico"}"]

    subprocess.run(args,check=True)


if __name__ == "__main__":
    build()
