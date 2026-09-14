import time
from collections import OrderedDict


class TTLCache:
    """A least-recently-used cache whose entries expire after ``ttl``."""

    def __init__(self, capacity, ttl, clock=time.monotonic):
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        self.data = OrderedDict()

    def _purge_expired(self, now):
        """Remove every entry that is no longer live at ``now``."""
        expired = [
            key
            for key, (_, inserted_at) in self.data.items()
            if now - inserted_at >= self.ttl
        ]
        for key in expired:
            del self.data[key]

    def put(self, k, v):
        if self.capacity <= 0:
            return

        now = self.clock()
        self._purge_expired(now)

        # Updating an existing key must not evict another key.  Replacing the
        # value also starts a fresh TTL and makes the key most recently used.
        self.data.pop(k, None)
        self.data[k] = (v, now)

        if len(self.data) > self.capacity:
            self.data.popitem(last=False)

    def get(self, k, default=None):
        now = self.clock()
        self._purge_expired(now)

        entry = self.data.get(k)
        if entry is None:
            return default

        v, inserted_at = entry
        if now - inserted_at >= self.ttl:
            del self.data[k]
            return default

        # Moving the key changes recency only; its original timestamp is kept
        # so a successful read never extends the TTL.
        self.data.move_to_end(k)
        return v
