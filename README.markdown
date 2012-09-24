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

Open a flask web-app [http://localhost:5000] exposing report data as JSON:
```sh
$ neurotic web
```

You can also, list test data, on console:

```
$ neurotic
{
    "longrepr": {
        "sections": [], 
        "reprcrash": {
            "path": "/Users/felipecruz/Projects/loogica/neurotic/tests/test_report_plugin.py", 
            "message": "assert 1 == [1, 2]", 
            "lineno": 5
        }, 
        "reprtraceback": {
            "reprentries": [
                {
                    "reprfuncargs": {
                        "args": []
                    }, 
                    "reprlocals": null, 
                    "lines": [
                        "    def test_pytest_report_teststatus_error():", 
                        ">       assert 1 ==[1, 2]", 
                        "E       assert 1 == [1, 2]"
                    ], 
                    "reprfileloc": {
                        "path": "tests/test_report_plugin.py", 
                        "message": "AssertionError", 
                        "lineno": 5
                    }, 
                    "short": false
                }
            ], 
            "style": "long", 
            "extraline": null
        }
    }, 
    "when": "call", 
    "nodeid": "tests/test_report_plugin.py::test_pytest_report_teststatus_error", 
    "duration": 0.0005729198455810547, 
    "location": [
        "tests/test_report_plugin.py", 
        3, 
        "test_pytest_report_teststatus_error"
    ], 
    "keywords": {
        "test_pytest_report_teststatus_error": 1
    }, 
    "outcome": "failed", 
    "sections": []
}
```

## Contact

felipecruz@loogica.net
