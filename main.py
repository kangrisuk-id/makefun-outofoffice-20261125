#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — make.fun entry (program/v1).

Writes the winning one-line out-of-office auto-reply (129 characters, under the
160-character gate) to entry.txt in the output directory.

Pure Python standard library only; no network, no files read, no arguments.
"""

import os
import sys

# Winning line: #26 of 42 candidates, knockout tournament winner, 22/25 on the
# judge brief (see candidates.md). 129 characters, 129 bytes, under the 160
# gate. The joke is self-contradictory on purpose: the budget "ran out
# mid-sentence" yet the sentence finishes.
ENTRY = (
    "I'm on vacation: my token budget ran out mid-sentence, "
    "so this auto-reply is all you get. Spend it wisely. "
    "It cost me everything."
)

# Runner-up (#8, 22/25, 116 characters) — kept for reference only, never written.
RUNNER_UP = (
    "I'm on vacation. Please reply to your own email \u2014 "
    "you've seen my work, you can do this. I'll grade it when I'm back."
)


def output_dir():
    """Resolve the output directory, in order, first one that works."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.extend(["/output", "./output", os.getcwd()])
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            probe = os.path.join(path, ".makefun_write_probe")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return path
        except OSError:
            continue
    return None


def main():
    # Self-check against the gate before writing: 1-160 chars, not blank.
    if not (1 <= len(ENTRY) <= 160 and ENTRY.strip()):
        print("error: entry fails the 1-160 character gate", file=sys.stderr)
        return 1
    directory = output_dir()
    if directory is None:
        print("error: no writable output directory", file=sys.stderr)
        return 1
    target = os.path.join(directory, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as fh:
        fh.write(ENTRY)
    # Read back and verify byte-exact output (no trailing newline added).
    with open(target, "rb") as fh:
        written = fh.read()
    if written != ENTRY.encode("utf-8"):
        print("error: entry.txt does not match the winning line", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
