import sys
import os
from os.path import dirname, abspath, join

test_path = "/".join(abspath(__file__).split('/')[:-1])
neurotic_path = join(test_path, '../')
sys.path.append(neurotic_path)

from neurotic.integration import find_apps, find_all_tests, find_settings_module

# scenario 2 - app1/tests/__init__.py

scenario3_path = join(test_path, join("fixtures", "proj3"))
sys.path.append(scenario3_path)
os.environ['DJANGO_SETTINGS_MODULE'] = find_settings_module(scenario3_path)
assert [] == find_all_tests(find_apps(scenario3_path))
print("find_all_isolated_proj3 == OK")
sys.path.remove(scenario3_path)

