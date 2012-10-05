from neurotic.domain import TestReportRepository

def test_test_report_repository():
    repository = TestReportRepository()

    assert repository.reports == []
    assert repository.report_counter == 0
    assert repository.run_counter == 0
    assert repository.last_run == 0

def test_test_report_start_run():
    repository = TestReportRepository()
    repository.start_run()

    assert repository.reports == [{'id': 1, 'reports': []}]
    assert repository.report_counter == 0
    assert repository.run_counter == 1
    assert repository.last_run == 0

def test_test_report_repository_add_report():
    repository = TestReportRepository()
    repository.start_run()
    repository.add_report({}) #opaque report

    assert repository.reports == [{'id': 1, 'reports': [{'id': 1}]}]
    assert repository.report_counter == 1
    assert repository.run_counter == 1
    assert repository.last_run == 0

    repository.add_report({}) #opaque report

    assert repository.reports == [{'id': 1, 'reports': [{'id': 1}, {'id': 2}]}]
    assert repository.report_counter == 2
    assert repository.run_counter == 1
    assert repository.last_run == 0

def test_test_report_show_failed_tests():
    repository = TestReportRepository()
    repository.start_run()
    repository.add_report({'outcome': 'failed'}) #opaque report
    repository.add_report({'outcome': 'passed'}) #opaque report
    repository.add_report({'outcome': 'failed'}) #opaque report

    assert list(repository.failed_tests()) == [{'id' : 1,
                                                'outcome': 'failed'},
                                               {'id': 3,
                                                'outcome': 'failed'}]

def test_test_report_last_run_failed_tests():
    repository = TestReportRepository()

    repository.start_run()
    repository.add_report({'outcome': 'failed', 'location': ['group']})
    repository.add_report({'outcome': 'passed', 'location': ['group']})
    repository.add_report({'outcome': 'failed', 'location': ['group']})

    assert list(repository.failed_tests()) == [{'id' : 1,
                                                'outcome': 'failed',
                                                'location': ['group']},
                                               {'id': 3,
                                                'outcome': 'failed',
                                                'location': ['group']}]

    # dummy finish
    repository.finish_run()
    assert repository.run_counter == 1

    repository.start_run()
    repository.add_report({'outcome': 'failed', 'location': ['group']}) #opaque report
    repository.add_report({'outcome': 'passed', 'location': ['group']}) #opaque report

    assert list(repository.last_run_failed_tests()) == [{'id' : 4,
                                                         'location': ['group'],
                                                         'outcome': 'failed'}]

    # dummy finish
    repository.finish_run()
    assert repository.run_counter == 2
