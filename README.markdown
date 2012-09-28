# neurotic

neurotic is a set of test tools to improve your daily test work.

This tools are:

* Test Report Collector - collect test reports and save them.
* Auto-Test - test when a file is modified or set a timer. 
* Async Test Runner - test and get asynchronous feedback.

## Install

```sh
$ python setup.py install
$ pip install -r requirements.txt
```

## Filosophy

## File Monitor

For testing purposes, neurotic will monitor file changes insidte ``tests``
directory, like ``test_report_plugin``. When you modify this file or
any other file insite ``tests`` dir neurotic will run silenly your test
suite (nowdays it'll run it's own tests using ``make test``)

To start neurotic file monitor just:

```sh
$ neurotic monitor
```

### Test Report Collector

neurotic is a pytest plugin that collects reports and save them to posteriour
queries.

A convenient command line tool will help you to visualize your saved tests 
reports.

For instance, run neurotic tests:

```sh
$ py.test -v .
```

Ant then.. last run test reports, on console:

```
$ neurotic
SUCCESS - tests/test_domain.py::test_test_report_repository
SUCCESS - tests/test_domain.py::test_test_report_start_run
SUCCESS - tests/test_domain.py::test_test_report_repository_add_report
SUCCESS - tests/test_domain.py::test_test_report_show_failed_tests
SUCCESS - tests/test_domain.py::test_test_report_last_run_failed_tests
SUCCESS - tests/test_report_plugin.py::test_pytest_report_teststatus
SUCCESS - tests/test_report_plugin.py::test_pytest_report_teststatus_error
```

### HTTP API to expore tests reports and runs

Open a flask web-app [http://localhost:5000] exposing report data as JSON:
```sh
$ neurotic web
```

## Contact

felipecruz@loogica.net
