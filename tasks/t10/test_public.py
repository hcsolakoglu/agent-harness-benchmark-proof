from ledger import apply_batch
s={'a':5}; assert apply_batch(s,[('add','a',2)])['a']==7
print('PUBLIC_OK')
