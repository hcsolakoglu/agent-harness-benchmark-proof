import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, capacity, ttl, clock=time.monotonic):
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        self.data = OrderedDict()
        self._expiries = OrderedDict()

    def put(self, k, v):
        if self.capacity <= 0:
            return
        now = self.clock()
        self._purge_expired(now)
        if k in self.data:
            del self.data[k]
            del self._expiries[k]
        while len(self.data) >= self.capacity:
            evicted, _ = self.data.popitem(last=False)
            del self._expiries[evicted]
        self.data[k] = (v, now)
        self._expiries[k] = now

    def get(self, k, default=None):
        if k not in self.data:
            return default
        v, t = self.data[k]
        if self.clock() - t >= self.ttl:
            del self.data[k]
            del self._expiries[k]
            return default
        self.data.move_to_end(k)
        return v

    def _purge_expired(self, now):
        expiries = self._expiries
        while expiries:
            k, t = next(iter(expiries.items()))
            if now - t < self.ttl:
                break
            del expiries[k]
            del self.data[k]
