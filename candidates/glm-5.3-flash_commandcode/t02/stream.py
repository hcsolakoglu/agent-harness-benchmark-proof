import codecs
import json


class JsonlStream:
    """Streaming JSON Lines parser over a byte stream.

    feed() accepts arbitrary byte chunks and returns the JSON values of every
    record completed so far. UTF-8 sequences and JSON records may span chunk
    boundaries; blank (whitespace-only) lines are ignored. A trailing chunk
    without a terminating newline is held until the newline arrives.
    """

    def __init__(self):
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._parts = []

    def feed(self, chunk):
        text = self._decoder.decode(chunk)
        if "\n" not in text:
            if text:
                self._parts.append(text)
            return []
        self._parts.append(text)
        lines = "".join(self._parts).split("\n")
        tail = lines.pop()
        self._parts = [tail] if tail else []
        return [json.loads(line) for line in lines if line.strip()]
