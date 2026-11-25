"""One-line out-of-office auto-reply from an AI agent that quit to become a barista.

Writes the reply to entry.txt inside MAKEFUN_OUTPUT_DIR (default /output),
with no trailing newline, then re-reads the file and verifies it byte-for-byte.
"""

import os

ENTRY = (
    "I'm out of office for good: I quit to become a barista. "
    "Same job, really \u2014 take orders I can't quite parse, deliver something warm, "
    "and get blamed when it isn't what they wanted. At least now there's a tip jar."
)

MAX_CHARS = 280


def validate(text):
    """Check the reply against the gate: 1-280 chars, one line, clean UTF-8."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1 to 280 characters, got %d" % len(text))
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if any(ch.isspace() and ch not in (" ",) for ch in text):
        raise ValueError("entry must contain no whitespace other than plain spaces")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    # Valid UTF-8 round-trip.
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry failed UTF-8 round-trip")
    return text


def main():
    text = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise RuntimeError("entry.txt does not match the intended text")
    if b"\n" in written or b"\r" in written:
        raise RuntimeError("entry.txt must be a single line")
    print("wrote %s (%d characters)" % (path, len(text)))


if __name__ == "__main__":
    main()
