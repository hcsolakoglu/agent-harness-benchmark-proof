import json


class JsonlStream:
    def __init__(self):
        self._partial = []

    def feed(self, chunk):
        out = []
        data = chunk
        partial = self._partial
        start = 0
        size = len(data)
        while start < size:
            end = data.find(b"\n", start)
            if end < 0:
                partial.append(data[start:])
                break
            segment = data[start:end]
            if partial:
                partial.append(segment)
                line = b"".join(partial)
                partial.clear()
            else:
                line = segment
            if line.endswith(b"\r"):
                line = line[:-1]
            if line and not line.isspace():
                out.append(json.loads(line))
            start = end + 1
        return out
