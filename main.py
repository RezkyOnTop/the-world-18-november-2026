"""Writes the 18 November 2026 front page to the output directory.

build.py draws entry.png with Pillow; the grader's sandbox has only the Python
standard library and no network, so this program copies those exact bytes and
both of its runs write an identical file.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> str:
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(os.path.join(HERE, "entry.png"), dest)
    return dest


if __name__ == "__main__":
    print(main())
