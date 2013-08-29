import imp
import json
import logging
import os
import pytest

try:
    nose_present = True
    from nose.plugins.base import Plugin
except:
    nose_present = False

from copy import deepcopy

from coopy.base import init_persistent_system

from .domain import TestReportRepository

repository = init_persistent_system(TestReportRepository,
                                    basedir="build_history")

def pytest_configure(config):
    config.pluginmanager.register(NeuroticReporter(config))

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = todict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__") and not isinstance(obj, tuple) \
         and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


def parse_nodeid(nodeid):
    blocks = nodeid.split('::')
    module, test_case, func = None, None, None

    if len(blocks) == 3:
        module, test_case, func = blocks
    elif len(blocks) == 2:
        module, func = blocks
    else:
        raise Exception("Unknow nodeid format")

    return dict(test_module=module, test_case=test_case, func=func)


def extract_docstr(blocks):
    custom_test_module_name = '_neurotic_temp'
    _temp = imp.load_source(custom_test_module_name, blocks['test_module'])

    test_case = blocks['test_case']
    func = blocks['func']
    docstrs = {}

    if test_case:
        docstrs['class_docstr'] = getattr(_temp, test_case).__doc__
        docstrs['func_docstr'] = getattr(getattr(_temp, test_case), func).__doc__
    else:
        docstrs['class_docstr'] = None
        docstrs['func_docstr'] = getattr(_temp, func).__doc__

    return docstrs


class NeuroticReporter(object):
    def __init__(self, config):
        self.config = config

    def pytest_report_teststatus(self, report):
        blocks = parse_nodeid(report.nodeid)
        docstr = extract_docstr(blocks)
        if report.when == "call":
            report_copy = deepcopy(report)
            report_dict = todict(report_copy)
            report_dict['docstring'] = docstr
            repository.add_report(report_dict)

    def pytest_report_header(config):
        repository.start_run()

    def pytest_terminal_summary(reporter):
        repository.finish_run()

if nose_present:
    import traceback
    from nose.case import FunctionTestCase, MethodTestCase

    class NeuroticNosePlugin(Plugin):
        name = "neurotic"
        enabled = True
        score = 9

        def __init__(self):
            super(NeuroticNosePlugin, self).__init__()
            self.reports = []
            self.current_context = None
            self.current_test = None
            self.current_file = None
            self.current_path = None

        def _extract_test_info(self, test):
            id = test.id()
            test_type = None
            test_name = id
            test_class_name = None
            test_method_name = None

            if isinstance(test.test, FunctionTestCase):
                test_name = test_name.split('.')[-1:][0]
                test_type = FunctionTestCase
                return (test_type, test_name, None, None)
            elif isinstance(test.test, MethodTestCase):
                test_class_name = test_name.split('.')[-2:-1][0]
                test_method_name = test_name.split('.')[-1:][0]
                test_name = '.'.join(test_name.split('.')[-2:])
                test_type = MethodTestCase
                return (test_type, test_name, test_class_name,
                                              test_method_name)

            raise Exception("Unkown Test Type")

        def _crete_base_report_info(self, test):
            test_info = self._extract_test_info(test)
            base_report = {
                'nodeid': str(test.id()),
                'location': [self.current_file, 0, test_info[1]],
                'keywords': '',
                'id': len(self.reports) + 1
            }
            return base_report

        def _extract_error_report(self, err):
            exctype, value, tb = err

            tb_info = traceback.extract_tb(tb)[2]
            tb_report = {
                'path':  str(tb_info[0]),
                'test_name': str(tb_info[2]),
                'lineno': str(tb_info[1]),
                'message': str(tb_info[3])
            }

            return dict(reprcrash=tb_report)

        def addSuccess(self, test):
            report = self._crete_base_report_info(test)
            report['outcome'] = 'passed'

            self.reports.append(report)

        def addError(self, test, err):
            report = self._crete_base_report_info(test)
            report['outcome'] = 'error'

            err_info = self._extract_error_report(err)
            report['longrepr'] = err_info

            self.reports.append(report)

        def addFailure(self, test, err):
            report = self._crete_base_report_info(test)
            report['outcome'] = 'failed'

            err_info = self._extract_error_report(err)
            report['longrepr'] = err_info

            self.reports.append(report)

        def finalize(self, result):
            tests_number = result.testsRun

            if not result.wasSuccessful():
                pass
            else:
                pass

            for report in self.reports:
                self.stream.writeln(json.dumps(report, indent=4))

        def setOutputStream(self, stream):
            self.stream = stream
            class dummy:
                def write(self, *arg):
                    pass
                def writeln(self, *arg):
                    pass
                def flush(self, *args):
                    pass
            d = dummy()
            return d

        def startContext(self, ctx):
            try:
                n = ctx.__name__
            except AttributeError:
                n = str(ctx).replace('<', '').replace('>', '')
                self.current_context = str(ctx)
            try:
                self.current_file = str(ctx.__file__).replace('.pyc', '.py')
                self.current_path = os.getcwd() + '/'
                self.current_file = self.current_file.replace(self.current_path, '')
            except AttributeError:
                pass

        def stopContext(self, ctx):
            self.current_context = None

        def startTest(self, test):
           self.current_test = test

        def stopTest(self, test):
            self.current_test = None
