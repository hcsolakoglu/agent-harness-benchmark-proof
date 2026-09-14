from safejoin import safe_join
from pathlib import Path
r=Path('/tmp/root'); assert safe_join(r,'a/b')==r/'a/b'
print('PUBLIC_OK')
