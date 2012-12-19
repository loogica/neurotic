# neurotic

neurotic is a set of test tools to improve your daily test work.

This tools are:

* Test Report Collector - collect test reports and build test runs result history.
* Auto-Test - test when a file is modified or set a timer. 

## Install

```sh
$ python setup.py install
$ pip install -r requirements.txt
```

## Philosophy

Software Testing should be AUTOMATIC.
Test Results should be tracked for further analysis.

## File Monitor

You have to specify wich directories willl going to be watched by neurotic.

```sh
$ neurotic monitor [directory list]
```

To watch `current` dir and the `tests` dir:

```sh
$ neurotic monitor . tests/ 
```

### Test Report Collector

neurotic provides both pytest and nose plugins to collect tests results in JSON,
and build a history.

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

*Flask and Jinja2 are dependencies for this feature*

Open a flask web-app [http://localhost:5000] exposing report data as JSON:

```sh
$ neurotic web
```

## TODO

* AsyncRunner currently runs "make test" - This should be configurable.
* Provide an way to `neurotic monitor` watch all subdirs from current dir.
* Improve Command Line feedbacks.
* Build cool UI to visualize reports history.
* Make cool sutff to extract useful information from results history.

## Contact

felipecruz@loogica.net
