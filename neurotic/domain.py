import json

from coopy.decorators import readonly

class TestReportRepository(object):
    def __init__(self):
        self.reports = []
        self.counter = 0
        self.last = 0

    def add_report(self, report):
        self.counter += 1
        report['id'] = self.counter
        self.reports.append(report)

    @readonly
    def show_history(self, size=1):
        data =  self.reports[self.last:]
        self.last = len(self.reports)
        for report in data:
            print(json.dumps(report, indent=4))
