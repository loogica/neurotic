from datetime import datetime

from neurotic.domain import TestReportRepository
from coopy.tests.utils import TestSystemMixin

class SystemFactory(TestSystemMixin):
    def __init__(self, date):
        self.date = date

    def get_domain(self, klass):
        obj = klass()
        self.mock_clock(obj, self.date)
        return obj

generic_date = datetime.now()
factory = SystemFactory(generic_date)

def test_test_report_repository__init():
    repository = factory.get_domain(TestReportRepository)

    assert repository.reports == []
    assert repository.report_counter == 0
    assert repository.run_counter == 0
    assert repository.last_run == 0

def test_test_report_start_run():
    repository = factory.get_domain(TestReportRepository)
    repository.start_run()

    assert repository.reports == [{'id': 1, 'reports': [],
                                   'start': generic_date}]
    assert repository.report_counter == 0
    assert repository.run_counter == 0
    assert repository.last_run == 0

def test_test_report_repository_add_report():
    repository = factory.get_domain(TestReportRepository)
    repository.start_run()
    repository.add_report({}) #opaque report

    assert repository.reports == [{'id': 1, 'start': generic_date,
                                   'reports': [{'id': 1,
                                                'when': generic_date}]}]
    assert repository.report_counter == 1
    assert repository.run_counter == 1
    assert repository.last_run == 0

    repository.add_report({}) #opaque report

    assert repository.reports == [{'id': 1, 'start': generic_date,
                                   'reports': [{'id': 1, 'when': generic_date},
                                               {'id': 2, 'when': generic_date}]}]
    assert repository.report_counter == 2
    assert repository.run_counter == 1
    assert repository.last_run == 0

def test_test_report_show_failed_tests():
    repository = factory.get_domain(TestReportRepository)
    repository.start_run()
    repository.add_report({'outcome': 'failed'}) #opaque report
    repository.add_report({'outcome': 'passed'}) #opaque report
    repository.add_report({'outcome': 'failed'}) #opaque report

    assert list(repository.failed_tests()) == [{'id' : 1,
                                                'outcome': 'failed',
                                                'when': generic_date},
                                               {'id': 3,
                                                'outcome': 'failed',
                                                'when': generic_date}]

def test_test_report_last_run_failed_tests():
    repository = factory.get_domain(TestReportRepository)

    repository.start_run()
    repository.add_report({'outcome': 'failed', 'location': ['group']})
    repository.add_report({'outcome': 'passed', 'location': ['group']})
    repository.add_report({'outcome': 'failed', 'location': ['group']})

    assert list(repository.failed_tests()) == [{'id' : 1,
                                                'outcome': 'failed',
                                                'location': ['group'],
                                                'when': generic_date},
                                               {'id': 3,
                                                'outcome': 'failed',
                                                'location': ['group'],
                                                'when': generic_date}]

    # dummy finish
    repository.finish_run()
    assert repository.run_counter == 1

    repository.start_run()
    repository.add_report({'outcome': 'failed', 'location': ['group']}) #opaque report
    repository.add_report({'outcome': 'passed', 'location': ['group']}) #opaque report

    assert list(repository.last_run_failed_tests()) == [{'id' : 4,
                                                         'location': ['group'],
                                                         'outcome': 'failed',
                                                         'when': generic_date}]

    # dummy finish
    repository.finish_run()
    assert repository.run_counter == 2
