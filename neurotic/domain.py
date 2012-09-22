import json

from coopy.decorators import readonly

class TestReportRepository(object):
    def __init__(self):
        self.reports = []

    def add_report(self, report):
        self.reports.append(report)

    @readonly
    def show_history(self, size=10):
        import json
        for report in self.reports[:size]:
            print(json.dumps(report, indent=4))
