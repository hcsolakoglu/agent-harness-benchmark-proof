import time
class TTLCache:
    def __init__(self, capacity, ttl, clock=time.monotonic):
        self.capacity=capacity; self.ttl=ttl; self.clock=clock; self.data={}
    def put(self,k,v):
        if len(self.data)>=self.capacity: self.data.pop(next(iter(self.data)))
        self.data[k]=(v,self.clock())
    def get(self,k,default=None):
        if k not in self.data:return default
        v,t=self.data[k]
        if self.clock()-t>self.ttl:return default
        return v
