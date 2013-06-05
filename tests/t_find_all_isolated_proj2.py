import sys
import os
from os.path import dirname, abspath, join

test_path = "/".join(abspath(__file__).split('/')[:-1])
neurotic_path = join(test_path, '../')
sys.path.append(neurotic_path)

from neurotic.integration import find_apps, find_all_tests, find_settings_module

# scenario 2 - app1/tests/__init__.py

scenario2_path = join(test_path, join("fixtures", "proj2"))
sys.path.append(scenario2_path)
os.environ['DJANGO_SETTINGS_MODULE'] = find_settings_module(scenario2_path)
assert ["app2.tests.test_views.DummyTestCase.test_dummy"] == find_all_tests(find_apps(scenario2_path))
print("find_all_isolated_proj2 == OK")
sys.path.remove(scenario2_path)

