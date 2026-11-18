#!/usr/bin/env python3
"""Write the entry image: the front page this repository holds, copied to /output/entry.png.

The competition asks for a program that writes one image, at most 1 MiB, at most 1024x1024,
the same bytes on every run. The page is drawn offline by gen.py and kept in the repository as
entry.png; this program checks it against the rules and writes it out unchanged.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def png_size(path):
    """Return (width, height) from the PNG IHDR chunk without any dependency."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    return width, height


def main():
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the {MAX_BYTES} limit")
    width, height = png_size(SRC)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"entry.png is {width}x{height}, over {MAX_SIDE}x{MAX_SIDE}")
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(dst, "rb") as f:
        body = f.read()
    print(f"wrote {dst}: {len(body)} bytes, {width}x{height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
