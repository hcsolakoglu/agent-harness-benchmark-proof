import sys
sys.path.insert(0,sys.argv[1]); from cache import TTLCache
now=[0.]; c=TTLCache(2,5,lambda:now[0]); c.put('a',1); now[0]=1;c.put('b',2); assert c.get('a')==1; c.put('c',3); assert c.get('b') is None and c.get('a')==1 and c.get('c')==3
now[0]=6; assert c.get('a') is None; c.put('d',4); c.put('e',5); assert c.get('d')==4 and c.get('e')==5
c.put('d',40); c.put('f',6); assert c.get('e') is None and c.get('d')==40
z=TTLCache(0,1,lambda:0); z.put('x',1); assert z.get('x') is None
print('HIDDEN_OK')
