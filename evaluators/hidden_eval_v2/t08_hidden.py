import sys
sys.path.insert(0,sys.argv[1]); from versions import newest
assert newest(['1.2.0','1.10.0'])=='1.10.0'
assert newest(['v2.0','1.99.9'])=='v2.0'
assert newest(['1.0.0-alpha','1.0.0','1.0.0-rc.2','1.0.0-rc.10'])=='1.0.0'
assert newest(['1.0.0+abc','1.0.0+xyz']) in {'1.0.0+abc','1.0.0+xyz'}
try:newest(['1.0','oops'])
except ValueError:pass
else:raise AssertionError
assert newest([]) is None
print('HIDDEN_OK')
