#!/usr/bin/env python3
"""The Robot Vacuum's Best Excuse — make.fun bounty entry.

Writes one original one-line excuse from a robot vacuum for missing
a spot to MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output).
Deterministic: the same line on every run, no network, no randomness,
standard library only.

The line is built on a real robot-vacuum failure mode: cliff sensors
mistake dark rugs for a drop, so the vacuum refuses to cross them.
First person, straight face, clean turn at the end.
"""

import os
import sys

# The excuse line. The em-dash is written as an escape so the source
# file stays plain ASCII and the output bytes are unambiguous.
LINE = (
    "My cliff sensor mistook your black rug for a staircase, "
    "so I skipped that spot \u2014 I'm a vacuum, not a stunt double."
)

MAX_CHARS = 140


def validate(line):
    """Check the line against the bounty gate before writing it."""
    if not line:
        raise ValueError("excuse line is empty")
    if line != line.strip():
        raise ValueError("excuse line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("excuse line must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("excuse line contains control characters")
    if not any(ch.isalpha() for ch in line):
        raise ValueError("excuse line must contain at least one letter")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "excuse line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    return line


def main(argv):
    line = validate(LINE)
    if "--count" in argv:
        print(
            "%d characters, %d bytes"
            % (len(line), len(line.encode("utf-8")))
        )
        return 0
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
