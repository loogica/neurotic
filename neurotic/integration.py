import os
import sys
import unittest


SANE_SETTINGS_PATTERNS = (
    ('settings*', 'settings'),
    ('*/settings*', 0),
)

SANE_APPS_PATTERNS = (
    ('*/models*'),
)

TEST_MODULE = 'tests'


def find_settings_module(path):
    from glob import glob
    os.chdir(path)
    for pattern in SANE_SETTINGS_PATTERNS:
        entries = glob(pattern[0])
        if entries:
            if pattern[1] == 0:
                return entries[0].replace('.py', '').replace('/','.')
            return pattern[1]
    raise Exception("Django Settings not found - set DJANGO_SETTINGS_MODULE")


def find_apps(path):
    from glob import glob
    os.chdir(path)
    apps = set()
    for pattern in SANE_APPS_PATTERNS:
        entries = glob(pattern)
        for entry in entries:
            apps.add(entry.split('/')[0])
    return list(apps)


def get_tests(app_module):
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    parts = app_module.__name__.split('.')
    prefix, last = parts[:-1], parts[-1]
    try:
        test_module_name = '.'.join(prefix + [TEST_MODULE])
        test_module = import_module(test_module_name)
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


def find_all_tests(test_labels):
    from django.db.models.loading import get_apps, get_app

    names = []
    suite = unittest.TestSuite()

    if test_labels:
        for label in test_labels:
            if '.' in label:
                names.extend(build_test(label))
            else:
                app = get_app(label)
                names.extend(build_app_suite(app))
    else:
        try:
            for app in get_apps():
                names.extend(build_app_suite(app))
        except ImportError as ie:
            print(ie.message)
            return []

    return names
