import heapq
import time
from collections import OrderedDict


class TTLCache:
    """LRU cache with a time-to-live.

    Semantics:
    - A successful get refreshes recency (LRU order) but not expiry.
    - put on an existing key refreshes both expiry and recency.
    - An entry is expired once its age is >= ttl; expired entries are purged
      lazily and never consume capacity.
    - A capacity <= 0 stores nothing.
    """

    def __init__(self, capacity, ttl, clock=time.monotonic):
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        self.data = OrderedDict()  # key -> (value, timestamp of last put)
        self._expiry = []          # min-heap of (timestamp, seq, key)
        self._seq = 0

    def _purge_expired(self, now):
        heap = self._expiry
        data = self.data
        ttl = self.ttl
        while heap:
            t, _, k = heap[0]
            if k not in data or data[k][1] != t:
                heapq.heappop(heap)  # stale: key was updated or evicted
                continue
            if now - t >= ttl:
                heapq.heappop(heap)
                del data[k]
            else:
                break  # heap is ordered by time, so nothing newer is expired

    def put(self, k, v):
        if self.capacity <= 0:
            return
        now = self.clock()
        self._purge_expired(now)
        data = self.data
        if k not in data:
            while len(data) >= self.capacity:
                data.popitem(last=False)
        data[k] = (v, now)
        data.move_to_end(k)
        self._seq += 1
        heapq.heappush(self._expiry, (now, self._seq, k))

    def get(self, k, default=None):
        entry = self.data.get(k)
        if entry is None:
            return default
        v, t = entry
        if self.clock() - t >= self.ttl:
            del self.data[k]
            return default
        self.data.move_to_end(k)
        return v
