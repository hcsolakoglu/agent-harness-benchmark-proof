"""Incremental decoder for JSONL (newline-delimited JSON) byte streams.

:class:`JsonlStream` is fed arbitrary byte chunks, as they arrive from a
socket or pipe.  Neither a JSON record nor a multi-byte UTF-8 code point is
guaranteed to fit inside a single chunk, so bytes are buffered until a
newline terminator is seen; only then is a line decoded and parsed.  Blank
lines (empty or whitespace-only) are ignored.
"""

from __future__ import annotations

import json
from typing import Any, List, Union

__all__ = ["JsonlStream"]

#: Sentinel returned by :func:`_parse_line` for lines that carry no record.
_BLANK = object()

#: Types accepted by :meth:`JsonlStream.feed`.
Chunk = Union[str, bytes, bytearray, memoryview]


def _parse_line(line: Union[bytes, bytearray]) -> Any:
    """Parse a single newline-terminated JSONL line.

    Returns ``_BLANK`` when the line is empty or whitespace-only.  Raises
    :class:`json.JSONDecodeError` for malformed JSON and
    :class:`UnicodeDecodeError` for invalid UTF-8.
    """
    if not line.strip():
        return _BLANK
    return json.loads(line)


class JsonlStream:
    """Emit complete JSONL records from arbitrarily chunked input.

    >>> stream = JsonlStream()
    >>> stream.feed(b'{"a": 1}\\n{"b":')
    [{'a': 1}]
    >>> stream.feed(b' 2}\\n')
    [{'b': 2}]

    Splitting the input anywhere -- in the middle of a record, a string, or a
    multi-byte UTF-8 code point -- produces exactly the same records as
    feeding the whole stream at once.  A trailing record that is not
    terminated by a newline stays buffered (it may still be completed by a
    later chunk); call :meth:`flush` at end of stream to emit it.
    """

    __slots__ = ("buf",)

    def __init__(self) -> None:
        # Bytes received but not yet forming a complete (newline-terminated)
        # line.  A bytearray keeps appends amortized O(1) and lets consumed
        # bytes be dropped without copying the retained remainder.
        self.buf = bytearray()

    def feed(self, chunk: Chunk) -> List[Any]:
        """Append *chunk* and return the records it completed, in order.

        Bytes after the last newline are retained for the next call, so an
        incomplete record is never parsed, never lost, and never emitted
        twice.  A malformed complete line raises and is discarded, leaving
        the stream usable for the following lines.
        """
        if isinstance(chunk, str):
            # Be forgiving about text input; the wire format is UTF-8 bytes.
            chunk = chunk.encode("utf-8")
        elif not isinstance(chunk, (bytes, bytearray, memoryview)):
            raise TypeError(
                "chunk must be bytes-like, not %s" % type(chunk).__name__
            )

        buf = self.buf
        buf.extend(chunk)

        records: List[Any] = []
        pos = 0
        try:
            while True:
                newline = buf.find(b"\n", pos)
                if newline < 0:
                    # No terminator left: buf[pos:] is a fragment that a later
                    # chunk may complete, so keep it for the next call.
                    break
                line = buf[pos:newline]
                pos = newline + 1
                record = _parse_line(line)
                if record is not _BLANK:
                    records.append(record)
        finally:
            # Drop consumed bytes even when a malformed line raised, so the
            # stream stays usable and buffered data is never parsed twice.
            del buf[:pos]
        return records

    def flush(self) -> List[Any]:
        """Emit a final record that end of stream left without a newline.

        JSONL producers are not required to terminate the last record, so
        this completes the stream.  Returns an empty list when nothing (or
        only whitespace) is buffered, and is idempotent.
        """
        buf = self.buf
        if not buf:
            return []
        line = bytes(buf)
        del buf[:]
        record = _parse_line(line)
        return [] if record is _BLANK else [record]

    @property
    def pending(self) -> bytes:
        """Bytes buffered so far that do not yet form a complete record."""
        return bytes(self.buf)

    def __repr__(self) -> str:
        return "%s(pending=%d bytes)" % (type(self).__name__, len(self.buf))
