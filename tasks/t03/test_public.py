from cache import TTLCache
now=[0.]; c=TTLCache(2,10,lambda:now[0]); c.put('a',1); assert c.get('a')==1
print('PUBLIC_OK')
