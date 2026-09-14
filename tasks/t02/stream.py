import json
class JsonlStream:
    def __init__(self): self.buf=b""
    def feed(self, chunk):
        self.buf += chunk
        out=[]
        for line in self.buf.decode().split("\n"):
            if line: out.append(json.loads(line))
        self.buf=b""
        return out
