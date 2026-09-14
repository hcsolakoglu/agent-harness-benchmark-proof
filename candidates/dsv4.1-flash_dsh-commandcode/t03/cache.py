"""A capacity-bounded cache with least-recently-used eviction and per-entry TTL."""

import heapq
import itertools
import time
from collections import OrderedDict

__all__ = ["TTLCache"]


class TTLCache:
    """Fixed-capacity cache with true LRU eviction and time-to-live expiry.

    Semantics
    ---------
    * An entry's *age* is ``clock() - written_at`` and it expires as soon as
      ``age >= ttl``; the boundary itself is already expired.
    * A successful ``get`` refreshes recency only: the key becomes the most
      recently used entry, but its age is untouched, so reading an entry can
      never keep it alive past ``written_at + ttl``.
    * ``put`` inserts or updates a key and refreshes both its write time
      (restarting its TTL) and its recency.
    * Expired entries are removed eagerly, so they never consume capacity:
      they are purged before any live entry is considered for LRU eviction.
    * ``capacity <= 0`` disables storage entirely; ``put`` stores nothing.

    Recency is tracked with an ``OrderedDict`` (least recently used first) and
    expirations with a lazy min-heap keyed by write time (the oldest write has
    the greatest age), keeping every operation ``O(log n)`` worst case instead
    of the ``O(n)`` scan a naive purge would require.
    """

    def __init__(self, capacity, ttl, clock=time.monotonic):
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        # key -> [value, written_at], ordered least recently used first.
        self.data = OrderedDict()
        # Min-heap of (written_at, sequence, key) used to find the oldest
        # entries in O(log n).  Records can be stale (a key was refreshed or
        # removed after being pushed); they are validated against the entry's
        # current write time when popped.  The strictly increasing sequence
        # keeps keys out of comparisons, so mixed key types stay orderable.
        self._writes = []
        self._sequence = itertools.count()

    def _expired(self, written_at, now):
        """True when an entry written at ``written_at`` has age >= ``ttl``."""
        return now - written_at >= self.ttl

    def _purge(self, now):
        """Drop every entry whose age has reached ``ttl``."""
        writes = self._writes
        data = self.data
        while writes and self._expired(writes[0][0], now):
            written_at, _, key = heapq.heappop(writes)
            entry = data.get(key)
            if entry is not None and entry[1] == written_at:
                del data[key]

    def _live_entry(self, key):
        """Return ``key``'s entry, dropping it if expired, or ``None``."""
        entry = self.data.get(key)
        if entry is None:
            return None
        if self._expired(entry[1], self.clock()):
            # Expired at age >= ttl: drop it so it cannot consume capacity.
            del self.data[key]
            return None
        return entry

    def _compact(self):
        """Rebuild the write heap so stale records cannot grow without bound."""
        self._writes = [
            (written_at, next(self._sequence), key)
            for key, (_, written_at) in self.data.items()
        ]
        heapq.heapify(self._writes)

    def put(self, key, value):
        """Insert or update ``key``, refreshing its value, TTL and recency."""
        if self.capacity <= 0:
            return
        now = self.clock()
        # Expired entries must never displace live ones or block a new write.
        self._purge(now)
        # Re-inserting moves the key to the most-recently-used end.
        self.data.pop(key, None)
        while len(self.data) >= self.capacity:
            self.data.popitem(last=False)
        self.data[key] = [value, now]
        heapq.heappush(self._writes, (now, next(self._sequence), key))
        if len(self._writes) > 2 * len(self.data) + 16:
            # Hot keys leave one stale record per rewrite; keep memory O(n).
            self._compact()

    def get(self, key, default=None):
        """Return ``key``'s value, or ``default`` when missing or expired."""
        entry = self._live_entry(key)
        if entry is None:
            return default
        self.data.move_to_end(key)  # refresh recency, not the write time
        return entry[0]

    def __contains__(self, key):
        # Membership is an observation, so it does not refresh recency.
        return self._live_entry(key) is not None

    def __len__(self):
        self._purge(self.clock())
        return len(self.data)
