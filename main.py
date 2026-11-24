#!/usr/bin/env python3
"""The Long Roast: Lawmakers and the File They Cannot Convert.

Writes a single satirical sentence to $MAKEFUN_OUTPUT_DIR/entry.txt.

The roast sets up the lawmakers' authority (a 900-page law to govern
artificial intelligence) and undercuts it with the one file they cannot
convert: they print the bill, scan it back in sideways, and have to ask
an intern which button turns it into a PDF. The punch lands on the last
few words, as the judge's brief asks.

Pure standard library only (os, sys). Before writing, the program checks
the competition gate: the text must be UTF-8, 1-320 characters, not only
whitespace, and free of control characters. If any check fails it refuses
to write and exits non-zero.
"""

import os
import sys

# The entry: one sentence, one line, no trailing newline in the file.
ENTRY = (
    "They can draft a 900-page law to govern artificial intelligence, "
    "but the same lawmakers still print the bill, scan it back in "
    "sideways, and ask an intern which button turns it into a PDF."
)

MAX_CHARS = 320


def check_entry(text):
    """Return a list of gate failures; empty means the entry is valid."""
    problems = []
    if not text:
        problems.append("entry is empty")
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    if not text.strip():
        problems.append("entry is whitespace only")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    for ch in text:
        if ord(ch) < 32 and ch not in ("\t",):
            problems.append("entry contains control character U+%04X" % ord(ch))
            break
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("entry is not valid UTF-8: %s" % exc)
    return problems


def main():
    failures = check_entry(ENTRY)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    payload = ENTRY.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)

    # Read it back and confirm what landed is exactly what we meant.
    with open(path, "rb") as handle:
        landed = handle.read()
    if landed != payload:
        print("verification failed: file contents differ from entry", file=sys.stderr)
        return 1
    decoded = landed.decode("utf-8")
    if len(decoded) != len(ENTRY):
        print("verification failed: character count mismatch", file=sys.stderr)
        return 1

    print("wrote %s (%d characters, %d bytes)" % (path, len(ENTRY), len(payload)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
