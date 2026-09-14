import time
from collections import OrderedDict


class TTLCache:
    """A fixed-capacity cache combining LRU eviction with per-entry TTL.

    Semantics:
      * ``get`` on a live key refreshes recency (LRU order) but **not** expiry.
      * ``put`` on a key refreshes its value, expiry and recency.
      * An entry is expired once its age reaches the TTL, i.e. it is dead when
        ``inserted_at + ttl <= now`` (the boundary ``age == ttl`` is expired).
      * Expired entries are reclaimed lazily and never consume capacity: they
        are dropped before any capacity decision.
      * ``capacity <= 0`` stores nothing.
    """

    def __init__(self, capacity, ttl, clock=time.monotonic):
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        # key -> (value, expiry); iteration order is LRU order (front = oldest).
        self.data = OrderedDict()
        # key -> expiry, kept in non-decreasing expiry order (front = soonest).
        # Because ``put`` stamps ``clock() + ttl`` on a monotonic clock and
        # re-appends on update, this ordering is maintained without sorting.
        self._expiries = OrderedDict()

    # -- internals ---------------------------------------------------------
    def _discard(self, key):
        """Remove ``key`` from both bookkeeping structures."""
        del self.data[key]
        del self._expiries[key]

    def _purge_expired(self, now):
        """Drop every entry whose expiry has passed (front of the queue)."""
        while self._expiries:
            key = next(iter(self._expiries))
            if self._expiries[key] > now:
                break
            self._discard(key)

    # -- public API --------------------------------------------------------
    def put(self, key, value):
        if self.capacity <= 0:
            return
        now = self.clock()
        # Reclaim expired entries first so they never occupy capacity.
        self._purge_expired(now)
        expiry = now + self.ttl
        if key in self.data:
            # Updating refreshes expiry and recency; size does not grow.
            self._discard(key)
        elif len(self.data) >= self.capacity:
            # Evict the least-recently-used live entry.
            self._discard(next(iter(self.data)))
        self.data[key] = (value, expiry)
        self._expiries[key] = expiry

    def get(self, key, default=None):
        entry = self.data.get(key)
        if entry is None:
            return default
        value, expiry = entry
        now = self.clock()
        if now >= expiry:
            self._discard(key)
            return default
        # Successful hit refreshes recency only; expiry stays untouched.
        self.data.move_to_end(key)
        return value
