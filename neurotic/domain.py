import json
from datetime import datetime

from coopy.decorators import readonly

class TestReportRepository(object):
    def __init__(self):
        self.reports = []
        self.run_counter = 0
        self.report_counter = 0
        self.last_run = 0

    def add_report(self, report):
        self.report_counter += 1
        report['id'] = self.report_counter
        self.current_report()['reports'].append(report)

    @readonly
    def show_history(self, size=1):
        data =  self.reports[self.last_run:]
        self.last_run = len(self.reports)
        for report in data:
            print(json.dumps(report, indent=4))

    @readonly
    def failed_tests(self, size=10):
        for run_report in self.reports:
            for report in run_report['reports']:
                if report['outcome'] == 'failed':
                    yield report

    @readonly
    def last_run_report_type(self, outcome_type="all"):
        for report in self.current_report()['reports']:
            if outcome_type == "all":
                yield report
            else:
                if report['outcome'] == outcome_type:
                    yield report

    def last_run_failed_tests(self):
        return self.last_run_report_type(outcome_type="failed")

    def last_run_good_tests(self):
        return self.last_run_report_type(outcome_type="passed")

    @readonly
    def current_report(self):
        if self.run_counter > 0:
            return self.reports[self.run_counter - 1]
        return None

    def start_run(self):
        self.run_counter += 1
        self.reports.append({'id': self.run_counter,
                             'reports': []})

    def finish_run(self):
        pass
