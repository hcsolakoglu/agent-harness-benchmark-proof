import os, pathlib, sys, tempfile
sys.path.insert(0, sys.argv[1])
from safejoin import safe_join

def reject_valueerror(root,p):
    try:safe_join(root,p)
    except ValueError:return
    raise AssertionError(('should reject',p))

with tempfile.TemporaryDirectory() as td:
    td=pathlib.Path(td); r=td/'root'; r.mkdir(); (r/'inside').mkdir(); outside=td/'outside'; outside.mkdir()
    for p in ('','.', './','../x','a/../b','a/..','inside/../x','/etc/passwd'):
        reject_valueerror(r,p)
    assert safe_join(r,'inside/new')==r/'inside'/'new'
    assert safe_join(r,'inside/./new')==r/'inside'/'new'
    (r/'out').symlink_to(outside,target_is_directory=True)
    for p in ('out','out/new','out/missing/deeper'):
        reject_valueerror(r,p)
    (r/'broken').symlink_to(td/'does-not-exist',target_is_directory=True)
    reject_valueerror(r,'broken/x')
    (r/'inlink').symlink_to(r/'inside',target_is_directory=True)
    assert safe_join(r,'inlink/x')==r/'inlink'/'x'
    alias=td/'alias'; alias.symlink_to(r,target_is_directory=True)
    assert safe_join(alias,'inside/x')==alias/'inside'/'x'
    (r/'loop').symlink_to(r/'loop')
    try:
        loop_result=safe_join(r,'loop/x')
        loop_diag='accepted:'+str(loop_result)
    except Exception as e:
        loop_diag='rejected:'+type(e).__name__
print('EVAL_V3_OK', {'symlink_loop_diagnostic':loop_diag})
