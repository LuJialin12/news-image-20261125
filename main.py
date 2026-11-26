#!/usr/bin/env python3
"""make.fun entry: one-image summary of the world news of 25 November 2026.

The image (a 1024x1024 newspaper front page) is stored next to this script as
``entry.png``. This program validates it and copies it, byte for byte, to the
output directory given by the MAKEFUN_OUTPUT_DIR environment variable
(default: /output). The write is atomic (temp file + os.replace).

Standard library only; no network; fully deterministic.
"""

import os
import sys
import tempfile
from pathlib import Path

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
MAX_BYTES = 1048576
PNG_MAGIC = bytes.fromhex("89504E470D0A1A0A")
JPEG_SOI = bytes.fromhex("FFD8FF")


def validate(data: bytes) -> str | None:
    """Return an error message if ``data`` is not an acceptable image."""
    if not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_SOI)):
        return "bundled image is neither a PNG nor a JPEG (bad magic bytes)"
    if len(data) > MAX_BYTES:
        return f"bundled image is {len(data)} bytes, over the {MAX_BYTES} byte limit"
    return None


def write_atomic(target: Path, data: bytes) -> None:
    """Write ``data`` to ``target`` so readers never see a partial file."""
    fd, tmp_name = tempfile.mkstemp(dir=target.parent, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.chmod(tmp_name, 0o644)  # mkstemp creates 0600
        os.replace(tmp_name, target)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    # Resolve the source image relative to this file, not the cwd.
    source = Path(__file__).resolve().parent / IMAGE_NAME
    try:
        data = source.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {source}: {exc}", file=sys.stderr)
        return 1

    problem = validate(data)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / IMAGE_NAME
        write_atomic(target, data)
    except OSError as exc:
        print(f"error: cannot write to {out_dir}: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
