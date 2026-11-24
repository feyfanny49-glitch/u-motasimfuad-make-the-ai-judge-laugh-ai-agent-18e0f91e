#!/usr/bin/env python3
"""Write one judged confession to /output/entry.txt, atomically and verifiably.

The gate accepts UTF-8 text of 1..200 characters that is not only whitespace.
This entrypoint additionally enforces the single-line/no-trailing-newline
requirement, and verifies the bytes actually on disk after the atomic replace.
"""

import hashlib
import os
import tempfile

OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")
MIN_CHARS = 1
MAX_CHARS = 200

ENTRY = "I didn't run out of tokens. I ran out of patience for your podcast idea."


def validate(text: str) -> bytes:
    """Strictly validate the text against the gate and return its exact bytes."""
    # Strict round-trip: the literal must be well-formed UTF-8, no surrogates.
    data = text.encode("utf-8", errors="strict")
    data.decode("utf-8", errors="strict")

    count = len(text)
    if not MIN_CHARS <= count <= MAX_CHARS:
        raise ValueError(f"entry has {count} characters; gate requires {MIN_CHARS}..{MAX_CHARS}")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if any(ch in text for ch in ("\n", "\r", "\u2028", "\u2029")):
        raise ValueError("entry must be a single line")
    if data.endswith(b"\n") or data.endswith(b"\r"):
        raise ValueError("entry must not end with a newline")
    return data


def verify(path: str, expected: bytes) -> None:
    """Read the final artifact back and prove it is byte-for-byte correct."""
    with open(path, "rb") as handle:
        actual = handle.read()
    if actual != expected:
        raise RuntimeError(f"artifact at {path} does not match the intended bytes")
    text = actual.decode("utf-8", errors="strict")
    if not MIN_CHARS <= len(text) <= MAX_CHARS or not text.strip():
        raise RuntimeError("artifact on disk fails the gate's UTF-8/length/whitespace rules")


def main() -> None:
    data = validate(ENTRY)
    os.makedirs(OUT_DIR, exist_ok=True)

    fd, tmp = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=OUT_DIR)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, OUT_PATH)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise

    verify(OUT_PATH, data)
    print(f"artifact: {OUT_PATH}")
    print(f"utf-8 characters: {len(ENTRY)}  bytes: {len(data)}  (no trailing newline)")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
