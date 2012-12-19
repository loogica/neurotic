import os
import sys
import unittest

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from django.db.models.loading import get_apps, get_app
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

TEST_MODULE = 'tests'

def get_tests(app_module):
    parts = app_module.__name__.split('.')
    prefix, last = parts[:-1], parts[-1]
    try:
        test_module = import_module('.'.join(prefix + [TEST_MODULE]))
    except ImportError:
        # Couldn't import tests.py. Was it due to a missing file, or
        # due to an import error in a tests.py that actually exists?
        # app_module either points to a models.py file, or models/__init__.py
        # Tests are therefore either in same directory, or one level up
        if last == 'models':
            app_root = import_module('.'.join(prefix))
        else:
            app_root = app_module

        if not module_has_submodule(app_root, TEST_MODULE):
            test_module = None
        else:
            # The module exists, so there must be an import error in the test
            # module itself.
            raise
    return test_module

def get_test_strings(tests):
    data = []
    if isinstance(tests, unittest.TestCase):
        return tests.id()
    elif isinstance(tests, unittest.TestSuite):
        for test in tests._tests:
            data.append(get_test_strings(test))

    return data


def build_app_suite(app_module):
    tests = None
    test_module = get_tests(app_module)
    if test_module:
        tests = unittest.defaultTestLoader.loadTestsFromModule(test_module)

    names = get_test_strings(tests)
    names = sum(names, [])

    return names


def build_suite(test_labels):
    names = []
    suite = unittest.TestSuite()

    if test_labels:
        for label in test_labels:
            if '.' in label:
                names.extend(uild_test(label))
            else:
                app = get_app(label)
                names.extend(build_app_suite(app))
    else:
        for app in get_apps():
            names.extend(build_app_suite(app))

    for name in names:
        print(name)

    import sys
    sys.exit(0)
