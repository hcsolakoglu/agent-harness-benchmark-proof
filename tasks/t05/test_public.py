from retry import retry
n=[0]
def f():
 n[0]+=1
 if n[0]<2: raise TimeoutError()
 return 7
assert retry(f,sleep=lambda _:None)==7
print('PUBLIC_OK')
