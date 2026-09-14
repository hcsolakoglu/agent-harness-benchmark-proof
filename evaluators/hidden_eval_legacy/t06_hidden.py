import sys,tempfile,pathlib,os
sys.path.insert(0,sys.argv[1]); from safejoin import safe_join
with tempfile.TemporaryDirectory() as td:
 r=pathlib.Path(td)/'root'; r.mkdir(); (r/'ok').mkdir();
 assert safe_join(r,'ok/x')==r/'ok'/'x'
 for p in ('../escape','/etc/passwd','ok/../../escape','.'):
  try: safe_join(r,p)
  except ValueError: pass
  else: raise AssertionError(p)
 outside=pathlib.Path(td)/'outside'; outside.mkdir(); (r/'link').symlink_to(outside,target_is_directory=True)
 try: safe_join(r,'link/file')
 except ValueError: pass
 else: raise AssertionError('symlink escape')
print('HIDDEN_OK')
