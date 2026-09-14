import json


class JsonlStream:
    def __init__(self):
        self.buf = bytearray()

    def feed(self, chunk):
        self.buf.extend(chunk)
        out = []
        consumed = 0

        while True:
            newline = self.buf.find(b"\n", consumed)
            if newline == -1:
                break

            line = self.buf[consumed:newline]
            consumed = newline + 1

            # Check for blank lines at the byte level so an incomplete or
            # split UTF-8 sequence is never decoded prematurely.
            if not line.strip():
                continue

            out.append(json.loads(bytes(line).decode("utf-8")))

        if consumed:
            del self.buf[:consumed]

        return out
