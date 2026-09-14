import sys
sys.path.insert(0,sys.argv[1]); from scheduler import schedule
assert schedule({'c':['a','b'],'b':['a'],'a':[]})==['a','b','c']
assert schedule({'z':[],'a':[]})==['a','z']
try: schedule({'a':['b'],'b':['a']})
except ValueError as e: assert 'cycle' in str(e).lower()
else: raise AssertionError('cycle not detected')
try: schedule({'a':['missing']})
except KeyError: pass
else: raise AssertionError('unknown dependency not detected')
# input must remain unchanged
g={'b':['a'],'a':[]}; before=repr(g); schedule(g); assert repr(g)==before
print('HIDDEN_OK')
