import json


class JsonlStream:
    """Incremental JSONL parser over an arbitrary byte-chunk stream.

    ``feed`` accepts any bytes-like chunk and returns the list of JSON values
    whose records have been fully received (i.e. terminated by ``\\n``).
    Chunks may split both UTF-8 codepoints and JSON records; any trailing
    incomplete bytes are buffered until the next call. Blank lines (empty or
    whitespace-only) are ignored.
    """

    __slots__ = ("buf",)

    def __init__(self):
        self.buf = bytearray()

    def feed(self, chunk):
        if not isinstance(chunk, (bytes, bytearray, memoryview)):
            raise TypeError(
                "chunk must be bytes-like, got %s" % type(chunk).__name__
            )
        data = self.buf
        data += chunk

        out = []
        start = 0
        # A record boundary is an ASCII LF; since 0x0A can never be part of a
        # multi-byte UTF-8 sequence, every byte before a newline is a complete
        # codepoint sequence and is safe to decode.
        while True:
            nl = data.find(b"\n", start)
            if nl == -1:
                break
            line = bytes(data[start:nl]).strip()
            start = nl + 1
            if line:
                out.append(json.loads(line.decode("utf-8")))

        if start:
            del data[:start]
        return out

    def flush(self):
        """Emit a final record left in the buffer at end-of-stream.

        Only call once no more chunks will arrive. Returns the parsed value of
        a trailing, non-newline-terminated record, or ``None`` if there is no
        such record.
        """
        line = bytes(self.buf).strip()
        self.buf.clear()
        if not line:
            return None
        return json.loads(line.decode("utf-8"))
