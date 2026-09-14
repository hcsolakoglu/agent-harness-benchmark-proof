import sys
sys.path.insert(0, sys.argv[1])
from versions import newest
chain=['1.0.0-alpha','1.0.0-alpha.1','1.0.0-alpha.beta','1.0.0-beta','1.0.0-beta.2','1.0.0-beta.11','1.0.0-rc.1','1.0.0']
for a,b in zip(chain,chain[1:]): assert newest([a,b])==b,(a,b)
assert newest(['1.2','1.2.0']) in {'1.2','1.2.0'}
assert newest(['1.2-alpha','1.2'])=='1.2'
assert newest(['v2.0','1.99.99'])=='v2.0'
assert newest(['1.0.0+abc','1.0.0+xyz']) in {'1.0.0+abc','1.0.0+xyz'}
assert newest(['1.0.0-2','1.0.0-10'])=='1.0.0-10'
for bad in ('','1','01.2.3','1.02.3','1.2.03','1.0.0-01','1.0.0-alpha..x','1.0.0+','V1.2.3','1.2.3 ','1.2.3-α','1٢.2.3'):
    try:newest([bad])
    except ValueError:pass
    else:raise AssertionError(('invalid accepted',bad))
for bad in (None,123,b'1.2.3'):
    try:newest([bad])
    except ValueError:pass
    except Exception as e:raise AssertionError(('wrong exception',bad,type(e).__name__))
    else:raise AssertionError(('invalid accepted',bad))
huge='9'*5001; huge2='1'+'0'*5001
assert newest([f'{huge}.0.0','2.0.0'])==f'{huge}.0.0'
assert newest([f'1.0.0-{huge}',f'1.0.0-{huge2}'])==f'1.0.0-{huge2}'
assert newest([]) is None
print('EVAL_V3_OK')
