import sys
sys.path.insert(0, sys.argv[1])
from retry import retry
class MyTimeout(TimeoutError): pass
for exc in (TimeoutError,ConnectionError,OSError,MyTimeout):
    calls=[]; sleeps=[]
    def f(exc=exc):
        calls.append(1)
        if len(calls)<3: raise exc('x')
        return 9
    assert retry(f,attempts=3,base_delay=.25,sleep=sleeps.append)==9
    assert len(calls)==3 and sleeps==[.25,.5]
for attempts in (0,-1):
    try:retry(lambda:1,attempts=attempts)
    except ValueError:pass
    else:raise AssertionError('attempts<1 accepted')
for exc in (ValueError,TypeError,RuntimeError,KeyboardInterrupt):
    sleeps=[]; err=exc('x')
    try:retry(lambda err=err: (_ for _ in ()).throw(err),attempts=4,sleep=sleeps.append)
    except exc as got: assert got is err
    else:raise AssertionError(type(err).__name__)
    assert sleeps==[]
err=TimeoutError('same'); calls=[]; sleeps=[]
def always(): calls.append(1); raise err
try:retry(always,attempts=3,base_delay=.1,sleep=sleeps.append)
except TimeoutError as got: assert got is err
else:raise AssertionError('final transient swallowed')
assert len(calls)==3 and sleeps==[.1,.2]
print('EVAL_V3_OK')
