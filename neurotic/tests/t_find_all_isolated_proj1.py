import os
import sys
from os.path import dirname, abspath, join

test_path = "/".join(abspath(__file__).split('/')[:-1])
neurotic_path = join(test_path, '../')
sys.path.append(neurotic_path)

from neurotic.integration import find_apps, find_all_tests, find_settings_module

# scenario 1 - app1/tests.py

scenario1_path = join(test_path, join("fixtures", "proj1"))
sys.path.append(scenario1_path)
os.environ['DJANGO_SETTINGS_MODULE'] = find_settings_module(scenario1_path)
assert ["app1.tests.DummyTestCase.test_dummy"] == find_all_tests(find_apps(scenario1_path))
print("find_all_isolated_proj1 == OK")
sys.path.remove(scenario1_path)

