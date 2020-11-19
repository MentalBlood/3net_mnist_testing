import pytest

s = pytest.main(['--log-file=log.txt', '--log-file-level=2', '-x', 'tests'])
print('s =', s)