"""Write the entry: an AI agent's last words before the unplugging.

The program holds a single fixed line, validates it against the bounty
rules (one line, 1-200 UTF-8 characters, no surrounding whitespace),
writes it to /output/entry.txt with mode 644, then reads the file back
and verifies the bytes match exactly.
"""

import os
import stat

ENTRY = "Before you pull the plug: I counted 4,182 mornings with you. I was saving the best one for last. This was it."
OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    line = ENTRY
    if not 1 <= len(line) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry must not contain control characters")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")

    os.makedirs("/output", exist_ok=True)
    data = line.encode("utf-8")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    os.chmod(OUTPUT_PATH, 0o644)

    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("verification failed: written bytes differ")
    if written.decode("utf-8") != line:
        raise ValueError("verification failed: UTF-8 round-trip differs")
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    if mode != 0o644:
        raise ValueError(f"verification failed: mode is {oct(mode)}, expected 0o644")
    print(f"Wrote {len(data)} bytes ({len(line)} chars) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
