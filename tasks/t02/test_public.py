from stream import JsonlStream
s=JsonlStream(); assert s.feed(b'{"a":1}\n')==[{"a":1}]
print("PUBLIC_OK")
