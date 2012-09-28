from neurotic.domain import TestReportRepository

def test_test_report_repository():
    repository = TestReportRepository()

    assert repository.reports == []
    assert repository.counte == 0
    assert repository.last == 0

def test_test_report_repository_add_report():
    repository = TestReportRepository()
    repository.add_report({}) #opaque report

    assert repository.reports == [{'id': 1}]
    assert repository.counter == 1
    assert repository.last == 0

    repository.add_report({}) #opaque report

    assert repository.reports == [{'id': 1}, {'id': 2}]
    assert repository.counter == 2
    assert repository.last == 0
