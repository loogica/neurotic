import pytest
import urllib2
import json
import jsonpickle

from coopy.base import init_persistent_system

from copy import deepcopy

from .domain import TestReportRepository

def pytest_configure(config):
    config.pluginmanager.register(NeuroticReporter(config))

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = todict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
            for key, value in obj.__dict__.iteritems()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj

class NeuroticReporter(object):
    def __init__(self, config):
        self.config = config

    def pytest_report_teststatus(self, report):
        if report.when == "call":
            report_copy = deepcopy(report)
            repository.add_report(todict(report_copy))

    def pytest_report_header(config):
        repository.start_run()

    def pytest_terminal_summary(reporter):
        repository.finish_run()

repository = init_persistent_system(TestReportRepository,
                                    basedir="build_history")
